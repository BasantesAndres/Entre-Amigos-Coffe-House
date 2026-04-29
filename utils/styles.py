import streamlit as st

def load_global_styles():
    st.markdown("""
    <style>
        .stApp {
            background: #f6f7fb;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f2430 0%, #252b39 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: white;
        }

        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            min-height: 120px;
            margin-bottom: 16px;
        }

        .card-title {
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 10px;
        }

        .card-value {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
        }

        .panel-box {
            background: white;
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            margin-top: 16px;
        }

        .panel-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 12px;
        }

        .login-box {
            max-width: 430px;
            margin: 70px auto;
            background: white;
            padding: 36px;
            border-radius: 22px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 12px 34px rgba(0,0,0,0.08);
        }

        .brand-title {
            text-align: center;
            font-size: 2.1rem;
            font-weight: 800;
            color: #ec4899;
            margin-bottom: 8px;
        }

        .brand-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e5e7eb;
            padding: 16px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            color: #334155 !important;
            font-weight: 700 !important;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #111827 !important;
        }

        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label,
        .stDateInput label,
        .stCheckbox label {
            color: #111827 !important;
            font-weight: 600 !important;
        }

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stDateInput input {
            border-radius: 12px !important;
        }

        p, label, span, div {
            color: inherit;
        }
    </style>
    """, unsafe_allow_html=True)