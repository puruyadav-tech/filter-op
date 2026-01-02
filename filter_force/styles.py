def get_custom_css():
    return """
    <style>
        /* MAIN BACKGROUND AND FONT */
        :root {
            --primary-color: #00d2ff;
            --secondary-color: #3a7bd5;
            --accent-color: #ff0099;
            --background-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-color: #f1f5f9;
        }

        html, body, .stApp {
            background-color: var(--background-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(58, 123, 213, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 0, 153, 0.15) 0%, transparent 40%);
            color: var(--text-color);
            font-family: 'Inter', sans-serif;
        }

        /* HIDE DEFAULT HEADER */
        header {visibility: hidden;}
        .main .block-container {padding-top: 2rem;}

        /* RESTORE SIDEBAR TOGGLE */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            color: var(--primary-color) !important;
            background-color: rgba(15, 23, 42, 0.5); 
            border-radius: 50%;
            padding: 4px;
            z-index: 100000;
        }

        /* HEADERS */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-weight: 700;
        }
        h1 {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            padding-bottom: 1rem;
        }
        
        /* CARDS / CONTAINERS (Glassmorphism) */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        div[data-testid="stMetric"] label {
            color: #94a3b8;
        }

        /* BUTTONS */
        .stButton > button {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 14px 0 rgba(0, 210, 255, 0.39);
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px 0 rgba(0, 210, 255, 0.23);
        }
        .stButton > button:active {
            transform: scale(0.98);
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #0b1120;
            border-right: 1px solid rgba(255,255,255, 0.05);
        }
        section[data-testid="stSidebar"] h1 {
            font-size: 20px !important;
            background: none;
            -webkit-text-fill-color: white;
            color: white !important;
        }

        /* INPUT FIELDS */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }

        /* DATAFRAME */
        div[data-testid="stDataFrame"] {
            background: transparent;
        }
        
        /* CUSTOM CLASSES FOR HTML */
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        .feature-title {
            font-weight: bold;
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: #fff;
        }
        .feature-desc {
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar {
            width: 10px;
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }

        /* FILE UPLOADER */
        div[data-testid="stFileUploader"] {
            padding: 2rem;
            border: 2px dashed rgba(0, 210, 255, 0.3);
            border-radius: 12px;
            background: rgba(30, 41, 59, 0.4);
            transition: all 0.3s ease;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: rgba(0, 210, 255, 0.8);
            background: rgba(30, 41, 59, 0.6);
        }
        div[data-testid="stFileUploader"] section {
            background-color: transparent !important;
        }
        div[data-testid="stFileUploader"] button {
             border: 1px solid rgba(255,255,255,0.2) !important;
             color: white !important;
        }
        
        /* ALERTS */
        div[data-baseweb="alert"] {
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .stAlert {
             background-color: rgba(15, 23, 42, 0.9) !important;
        }
    </style>
    """
