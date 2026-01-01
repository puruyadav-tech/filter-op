import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve
from imblearn.over_sampling import SMOTE
from scipy.sparse import hstack

import os
import joblib

@st.cache_data(ttl=3600)
def load_data():
    """Loads dataset from local file or GitHub raw link."""
    # Robust path handling - works regardless of CWD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, "data", "training_data.csv")
    
    # Try local file first (Robust offline mode)
    if os.path.exists(local_path):
        try:
            df = pd.read_csv(local_path)
            if 'fraudulent' in df.columns:
                return df
            else:
                st.warning("Local dataset corrupted (missing labels). Attempting to recover from web...")
        except Exception as e:
            st.error(f"Error reading local data: {e}")
    
    # Fallback to GitHub Raw (More reliable than Drive)
    url = "https://raw.githubusercontent.com/l05t0ka/Fraud-Job-Offers-Analysis/master/fake_job_postings.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        train_df = pd.read_csv(io.BytesIO(response.content))
        
        # Verify downloaded data too
        if 'fraudulent' not in train_df.columns:
             st.error("Web dataset also missing labels. Please check source.")
             return pd.DataFrame()

        # Optional: Save to local for next time
        try:
            os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
            train_df.to_csv(local_path, index=False)
        except:
            pass
    except Exception as e:
        st.error(f"Error loading training data from Web: {e}")
        train_df = pd.DataFrame()
    return train_df

@st.cache_data(ttl=3600)
def prepare_data(df):
    """Preprocesses the dataframe."""
    df = df.copy()
    
    # Fill NA
    for col in ['title', 'description', 'requirements', 'company_profile']:
        if col not in df.columns:
            df[col] = ''
        else:
            df[col] = df[col].fillna('')
            
    # Email features
    if 'email' in df.columns:
        df['email'] = df['email'].fillna('')
        df['email_domain'] = df['email'].apply(lambda x: x.split('@')[-1] if '@' in x else '')
        df['free_email'] = df['email_domain'].isin(['gmail.com', 'yahoo.com', 'hotmail.com']).astype(int)
    else:
        df['email_domain'] = ''
        df['free_email'] = 0
        
    # Text features
    df['text'] = (
        df['title'] + ' ' +
        df['description'] + ' ' +
        df['requirements'] + ' ' +
        df['company_profile']
    )
    
    # Structural features
    df['desc_len'] = df['description'].apply(len)
    df['word_count'] = df['description'].apply(lambda x: len(x.split()))
    df['num_digits_in_title'] = df['title'].apply(lambda x: sum(c.isdigit() for c in x))
    df['has_profile'] = (df['company_profile'] != '').astype(int)
    
    # Suspicious terms
    suspicious_words = ['money', 'wire', 'bitcoin', 'transfer', 'click']
    df['suspicious_terms'] = df['description'].apply(
        lambda x: int(any(term in x.lower() for term in suspicious_words))
    )
    
    return df

@st.cache_resource(ttl=86400) 
def train_model(train_df):
    """Trains the XGBoost model with caching."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_cache_path = os.path.join(base_dir, "data", "model_cache.pkl")
    local_data_path = os.path.join(base_dir, "data", "training_data.csv")
    
    # Try loading cached model
    if os.path.exists(model_cache_path):
        try:
            return joblib.load(model_cache_path)
        except:
            pass # Re-train if cache invalid

    if train_df.empty:
        # One last ditch attempt to find data if dataframe is empty but file exists
        if os.path.exists(local_data_path):
             train_df = pd.read_csv(local_data_path)
             try:
                # Basic validation
                if 'fraudulent' not in train_df.columns:
                    st.error("Training data is missing the 'fraudulent' column. Cannot train model.")
                    return None, None, 0.5
                train_df = prepare_data(train_df)
             except Exception as e:
                st.error(f"Error preparing data: {e}")
                return None, None, 0.5
        
        if train_df.empty:
            st.warning("Training data not found. Please upload data or ensure data/training_data.csv exists.")
            return None, None, 0.5
        
    if 'fraudulent' not in train_df.columns:
         st.error("Loaded data missing 'fraudulent' labels.")
         return None, None, 0.5

    X = train_df[['text', 'desc_len', 'word_count', 'num_digits_in_title', 'has_profile', 'suspicious_terms', 'free_email']]
    y = train_df['fraudulent']
    
    # TF-IDF
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    X_tfidf = tfidf.fit_transform(X['text'])
    
    # Combine features
    X_combined = hstack([X_tfidf, X.drop(columns='text').values])
    
    # Train/Val Split
    X_train, X_val, y_train, y_val = train_test_split(X_combined, y, test_size=0.2, stratify=y, random_state=42)
    
    # SMOTE
    X_res, y_res = SMOTE(random_state=42).fit_resample(X_train, y_train)
    
    # Model
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_res, y_res)
    
    # Optimal Threshold
    val_probs = model.predict_proba(X_val)[:, 1]
    p, r, thresholds = precision_recall_curve(y_val, val_probs)
    f1s = 2 * p * r / (p + r + 1e-6)
    best_threshold = thresholds[np.argmax(f1s)]
    
    # Cache the result
    try:
        os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
        joblib.dump((model, tfidf, best_threshold), model_cache_path)
    except Exception as e:
        print(f"Failed to cache model: {e}")
    
    return model, tfidf, best_threshold

def predict(test_df, model, tfidf, best_threshold):
    """Generates predictions on new data."""
    if model is None or tfidf is None:
        return None
        
    X_test = test_df[['text', 'desc_len', 'word_count', 'num_digits_in_title', 'has_profile', 'suspicious_terms', 'free_email']]
    X_test_tfidf = tfidf.transform(X_test['text'])
    X_test_combined = hstack([X_test_tfidf, X_test.drop(columns='text').values])
    
    test_df['fraud_probability'] = model.predict_proba(X_test_combined)[:, 1]
    test_df['fraud_predicted'] = (test_df['fraud_probability'] >= best_threshold).astype(int)
    
    return test_df
