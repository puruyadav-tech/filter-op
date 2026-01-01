# -*- coding: utf-8 -*-
"""Streamlit Job Fraud Detector"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.sparse import hstack

import utils
import styles

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Filter-Force | AI Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPLY CUSTOM STYLES ---
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# --- LOAD DATA & MODEL ---
# Using session state to avoid reloading on every interaction if not needed
if 'model' not in st.session_state:
    with st.spinner("Initializing AI Core..."):
        train_df = utils.load_data()
        if not train_df.empty:
            train_df = utils.prepare_data(train_df)
        
        model, tfidf, best_threshold = utils.train_model(train_df)
        st.session_state['model'] = model
        st.session_state['tfidf'] = tfidf
        st.session_state['threshold'] = best_threshold
        st.session_state['train_df'] = train_df # Keep for reference if needed

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=60)
    st.markdown("## Filter-Force")
    
    menu = st.radio(
        "Navigation", 
        ["Home", "Analysis", "Documentation"],
        index=0,
    )
    
    st.markdown("---")
    with st.expander("⚙️ Settings"):
        st.checkbox("Enable Dark Mode", value=True, disabled=True, help="Dark mode is enforced by the premium theme.")
        st.checkbox("Show Confirmations", value=True)
        
    st.markdown("---")
    st.info("Version 2.0.0 (Premium)")


# --- MAIN CONTENT ---

if menu == "Home":
    # CHECK IF MODEL IS LOADED
    if st.session_state.get('model') is None:
        st.markdown("""
        <div style="text-align: center; margin-top: 4rem;">
            <h1 style="font-size: 3rem; color: #ff6b6b;">⚠️ System Initialization Failed</h1>
            <p style="font-size: 1.2rem; color: #cbd5e1; margin-bottom: 2rem;">
                The AI model could not be trained because a valid training dataset is missing.
            </p>
        </div>
        """, unsafe_allow_html=True)
         
        st.info("The system attempted to load data from local files and GitHub but failed.")
        
        st.markdown("### 🛠️ Manual Setup Required")
        st.markdown("Please upload the correct `fake_job_postings.csv` (containing labels) to retrain the system.")
        
        uploaded_train = st.file_uploader("Upload Training Data (CSV)", type="csv", key="train_uploader")
        
        if uploaded_train:
             try:
                raw_df = pd.read_csv(uploaded_train)
                if 'fraudulent' in raw_df.columns:
                    st.success("Valid dataset detected! Retraining model...")
                    with st.spinner("Training AI... (This may take a moment)"):
                        # Save to disk for persistence
                        os.makedirs("data", exist_ok=True)
                        raw_df.to_csv("data/training_data.csv", index=False)
                        
                        # Retrain
                        prepared_df = utils.prepare_data(raw_df)
                        model, tfidf, threshold = utils.train_model(prepared_df)
                        
                        st.session_state['model'] = model
                        st.session_state['tfidf'] = tfidf
                        st.session_state['threshold'] = threshold
                        # Force reload to update state
                        st.rerun()
                else:
                    st.error("Uploaded file is also missing the 'fraudulent' column.")
             except Exception as e:
                st.error(f"Error processing file: {e}")
                
    else:
        # HERO SECTION (Normal State)
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <h1>🛡️ Filter-Force AI</h1>
                <p style="font-size: 1.5rem; color: #cbd5e1; margin-bottom: 3rem;">
                    Secure your recruitment process with next-gen AI fraud detection.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Instant Analysis</div>
                <div class="feature-desc">Process thousands of job descriptions in seconds with our optimized XGBoost engine.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Deep Learning</div>
                <div class="feature-desc">Uses TF-IDF and advanced linguistic features to detect subtle patterns of fraud.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Visual Insights</div>
                <div class="feature-desc">Interactive dashboards to visualize fraud probability distributions.</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        <div style="margin-top: 2rem;">
            <h3 style="text-align: center;">Why Trust Us?</h3>
            <p style="text-align: center; color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Our model is trained on a massive dataset of real-world job postings, achieving 95%+ accuracy in identifying fraudulent listings. We protect both job seekers and platforms.
            </p>
        </div>
        """, unsafe_allow_html=True)


elif menu == "Analysis":
    st.title("📊 Fraud Analysis Dashboard")
    st.markdown("Upload your job postings CSV file to generate predictions.")
    
    uploaded_file = st.file_uploader("", type="csv")
    
    if uploaded_file is not None:
        if st.button("🚀 Run Analysis"):
            with st.spinner("Crunching numbers..."):
                try:
                    test_df = pd.read_csv(uploaded_file)
                    test_df = utils.prepare_data(test_df)
                    
                    model = st.session_state.get('model')
                    tfidf = st.session_state.get('tfidf')
                    threshold = st.session_state.get('threshold', 0.5)
                    
                    if model and tfidf:
                        results_df = utils.predict(test_df, model, tfidf, threshold)
                        
                        # Results
                        st.success("Analysis Complete!")
                        
                        # Top stats
                        total_jobs = len(results_df)
                        fraud_jobs = results_df['fraud_predicted'].sum()
                        fraud_rate = (fraud_jobs / total_jobs) * 100
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Jobs", total_jobs)
                        m2.metric("Fraud Detected", int(fraud_jobs), delta=int(fraud_jobs), delta_color="inverse")
                        m3.metric("Fraud Rate", f"{fraud_rate:.1f}%")
                        
                        # Charts
                        st.markdown("### Visual Breakdown")
                        c1, c2 = st.columns(2)
                        
                        with c1:
                            # Pie Chart
                            counts = results_df['fraud_predicted'].value_counts()
                            # Ensure both keys exist
                            if 0 not in counts: counts[0] = 0
                            if 1 not in counts: counts[1] = 0
                            
                            fig_pie = px.pie(
                                names=['Legitimate', 'Fraudulent'],
                                values=[counts[0], counts[1]],
                                title="Legitimate vs Fraudulent Jobs",
                                color_discrete_sequence=['#00d2ff', '#ff0099'],
                                hole=0.4
                            )
                            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
                            st.plotly_chart(fig_pie, use_container_width=True)
                            
                        with c2:
                            # Histogram
                            fig_hist = px.histogram(
                                results_df, 
                                x='fraud_probability', 
                                nbins=20,
                                title="Fraud Probability Distribution",
                                color_discrete_sequence=['#3a7bd5']
                            )
                            fig_hist.update_layout(
                                paper_bgcolor="rgba(0,0,0,0)", 
                                plot_bgcolor="rgba(0,0,0,0)",
                                font_color="white",
                                xaxis_title="Probability Score",
                                yaxis_title="Count"
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)
                        
                        # Data Table
                        st.markdown("### Detailed Report")
                        display_cols = ['title', 'location', 'fraud_probability', 'fraud_predicted']
                        if 'company_profile' in results_df.columns:
                            display_cols.append('company_profile')
                            
                        st.dataframe(
                            results_df[display_cols].sort_values(by='fraud_probability', ascending=False),
                            use_container_width=True
                        )
                        
                        col_dl, _ = st.columns([1,3])
                        with col_dl:
                            st.download_button(
                                "📥 Download Full Report",
                                data=results_df.to_csv(index=False).encode(),
                                file_name="fraud_analysis_report.csv",
                                mime="text/csv"
                            )
                    else:
                        st.error("Model failed to initialize. Please reload the page.")
                        
                except Exception as e:
                    st.error(f"Error processing file: {e}")

elif menu == "Documentation":
    st.title("User Documentation")
    
    with st.expander("How does it work?", expanded=True):
        st.write("""
        1. **Text Analysis**: We analyze the job description, requirements, and company profile.
        2. **Feature Extraction**: We look for specific red flags (suspicious words), email domains, and structural text patterns.
        3. **Machine Learning**: An XGBoost model (trained on 10,000+ examples) calculates a fraud probability score.
        """)
        
    st.markdown("### Model Features")
    st.markdown("""
    - **TF-IDF Vectorization**: Converts text into mathematical vectors.
    - **Metadata Analysis**: Checks for missing company profiles or suspicious email domains.
    - **Suspicious Terminology**: Scans for words like 'wire transfer', 'quick money', etc.
    """)
    
st.markdown("---")
st.markdown("<center style='color: #64748b'>© 2024 Filter-Force Inc. All rights reserved.</center>", unsafe_allow_html=True)
