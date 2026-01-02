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

        /* ANIMATIONS */
        @keyframes gradient-bg {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        @keyframes pulse-glow {
            0% {box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.4);}
            70% {box-shadow: 0 0 0 10px rgba(0, 210, 255, 0);}
            100% {box-shadow: 0 0 0 0 rgba(0, 210, 255, 0);}
        }

        html, body, .stApp {
            background-color: var(--background-dark);
            background-image: 
                linear-gradient(125deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            background-size: 400% 400%;
            animation: gradient-bg 15s ease infinite;
            color: var(--text-color);
            font-family: 'Inter', sans-serif;
        }

        /* HEADER CONFIG - CRITICAL FIX */
        header {
            background-color: transparent !important;
            visibility: visible !important; /* Must be visible for children to work reliably */
        }
        
        /* Hide the decoration bar and the toolbar (hamburger menu) */
        header > .stAppDeployButton { display: none; }
        header > .stAppDecoration { display: none; }
        header > div[data-testid="stToolbar"] { 
            visibility: hidden; 
            display: none;
        }

        .main .block-container {
            padding-top: 2rem;
        }

        /* ROBUST SIDEBAR TOGGLE FIX */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 20px;
            left: 20px;
            
            visibility: visible !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            
            color: var(--primary-color) !important;
            background-color: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            
            border-radius: 50%;
            width: 44px; /* Slightly larger */
            height: 44px;
            z-index: 2147483647 !important; /* Maximum Z-Index */
            transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        [data-testid="stSidebarCollapsedControl"]:hover {
            transform: scale(1.15) rotate(180deg); /* Add playful rotation */
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
            background-color: rgba(30, 41, 59, 1);
        }
        
        /* Ensure the icon inside is also visible */
        [data-testid="stSidebarCollapsedControl"] > img,
        [data-testid="stSidebarCollapsedControl"] > svg {
            width: 24px !important;
            height: 24px !important;
            fill: var(--primary-color) !important;
            color: var(--primary-color) !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-weight: 700;
        }
        h1 {
            background: linear-gradient(to right, #00d2ff, #3a7bd5, #ff0099);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            padding-bottom: 1rem;
            background-size: 200% auto;
            animation: gradient-bg 5s linear infinite;
        }
        
        /* CARDS / CONTAINERS (Glassmorphism) */
        .glass-card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 210, 255, 0.3);
            box-shadow: 0 20px 40px -10px rgba(0, 210, 255, 0.15);
        }

        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.4);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: scale(1.02);
            border-color: rgba(255, 0, 153, 0.3);
        }
        div[data-testid="stMetric"] label {
            color: #94a3b8;
        }

        /* BUTTONS */
        .stButton > button {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 14px 0 rgba(0, 210, 255, 0.39);
        }
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 10px 30px 0 rgba(0, 210, 255, 0.45);
        }
        /* Pulse for primary actions if needed, or applying to all for now as effect */
        .stButton > button:active {
            transform: scale(0.95);
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
