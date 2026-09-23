import streamlit as st
import pandas as pd
import pyodbc
from pathlib import Path

# =====================================================
# COLOR PALETTE
# =====================================================

BG_MAIN = "#08111F"
BG_CARD = "#111827"
BORDER = "#1F2937"
GRID = "#334155"
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"

ACCENT_BLUE = "#3B82F6"
ACCENT_CYAN = "#22D3EE"
ACCENT_GREEN = "#10B981"
ACCENT_RED = "#EF4444"
ACCENT_AMBER = "#F59E0B"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_INDIGO = "#6366F1"

STATUS_COLORS = {
    "Completed": ACCENT_GREEN,
    "Processing": ACCENT_BLUE,
    "Cancelled": ACCENT_RED,
    "Returned": ACCENT_AMBER
}

REGION_PALETTE = [
    "#1D4ED8","#2563EB","#3B82F6","#60A5FA",
    "#93C5FD","#0EA5E9","#38BDF8","#7DD3FC"
]

PRODUCT_PALETTE = [
    "#6D28D9","#7C3AED","#8B5CF6","#A78BFA",
    "#C4B5FD","#4F46E5","#6366F1","#818CF8",
    "#A5B4FC","#C7D2FE"
]

# =====================================================
# DARK ENTERPRISE THEME
# =====================================================

def inject_theme():
    st.markdown(f"""
    <style>

    .stApp {{
        background:{BG_MAIN};
        color:{TEXT_MAIN};
    }}

    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {{
        background:{BG_MAIN} !important;
    }}

    section[data-testid="stSidebar"] {{
        background:{BG_CARD};
        border-right:1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color:{TEXT_MAIN} !important;
    }}

    /* KPI */

    div[data-testid="stMetric"] {{
        background:{BG_CARD};
        border:1px solid {BORDER};
        border-radius:16px;
        padding:18px;
    }}

    div[data-testid="stMetricLabel"] p {{
        color:{TEXT_MUTED} !important;
    }}

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {{
        color:{TEXT_MAIN} !important;
        opacity:1 !important;
        font-weight:700 !important;
    }}

    /* ===== SELECTBOX FINAL FIX ===== */

    div[data-testid="stSelectbox"] {{
        background: transparent !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background: #0B1220 !important;
        border-radius: 10px !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background: #0B1220 !important;
        background-color: #0B1220 !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
        color: {TEXT_MAIN} !important;
        box-shadow: none !important;
        min-height: 42px !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {{
        background: transparent !important;
        color: {TEXT_MAIN} !important;
    }}

    div[data-testid="stSelectbox"] span {{
        color: {TEXT_MAIN} !important;
        opacity: 1 !important;
    }}

    div[data-testid="stSelectbox"] input {{
        color: {TEXT_MAIN} !important;
        -webkit-text-fill-color: {TEXT_MAIN} !important;
    }}

    div[data-testid="stSelectbox"] svg {{
        fill: {TEXT_MAIN} !important;
    }}

    /* Dropdown */

    div[role="listbox"] {{
        background:{BG_CARD} !important;
        border:1px solid {BORDER} !important;
    }}

    div[role="option"] {{
        background:{BG_CARD} !important;
        color:{TEXT_MAIN} !important;
    }}

    div[role="option"]:hover {{
        background:{BORDER} !important;
    }}

    /* Plotly */

    div[data-testid="stPlotlyChart"] {{
        background:{BG_CARD};
        border:1px solid {BORDER};
        border-radius:16px;
        padding:10px;
    }}

    [data-testid="stDataFrame"] {{
        border-radius:14px;
        overflow:hidden;
    }}

    .block-container {{
        padding-top:1.5rem;
        padding-bottom:2rem;
    }}

    h1,h2,h3,p,span,label {{
        color:{TEXT_MAIN};
    }}

    hr {{
        border-color:{BORDER};
    }}

    </style>
    """, unsafe_allow_html=True)

# =====================================================
# PLOTLY LAYOUT
# =====================================================

def style_fig(fig, y_title="", x_title="", show_legend=True):

    fig.update_layout(
        title="",
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font_color=TEXT_MAIN,
        font_size=13,
        xaxis_title=x_title,
        yaxis_title=y_title,
        yaxis_gridcolor=GRID,
        xaxis_gridcolor=BG_CARD,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            y=1.10,
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MAIN,size=12)
        ),
        margin=dict(t=20,l=10,r=10,b=10),
        hoverlabel=dict(
            bgcolor=BG_CARD,
            font_color=TEXT_MAIN,
            bordercolor=BORDER
        )
    )

    fig.update_xaxes(color=TEXT_MAIN)
    fig.update_yaxes(color=TEXT_MAIN)

    return fig

# =====================================================
# SMART DATA LOADER
# =====================================================

@st.cache_data
def load_data():

    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=OIM_DB;"
            "UID=sa;"
            "PWD=sayan@12345;"
            "TrustServerCertificate=yes;"
        )

        df = pd.read_sql("SELECT * FROM enriched_orders", conn)
        conn.close()

    except Exception:

        BASE_DIR = Path(__file__).resolve().parents[2]
        csv_path = BASE_DIR / "data" / "enriched_orders.csv"

        df = pd.read_csv(csv_path)

    for col in ["order_date","expected_date","actual_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "customer_region" in df.columns:
        df["customer_region"] = (
            df["customer_region"]
            .fillna("Unknown")
            .str.title()
        )

    if "delivery_delay_days" in df.columns:
        df["delivery_delay_days"] = pd.to_numeric(
            df["delivery_delay_days"],
            errors="coerce"
        ).fillna(0)

    return df
