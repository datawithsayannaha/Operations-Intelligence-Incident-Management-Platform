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
    "#1D4ED8", "#2563EB", "#3B82F6", "#60A5FA",
    "#93C5FD", "#0EA5E9", "#38BDF8", "#7DD3FC"
]

PRODUCT_PALETTE = [
    "#6D28D9", "#7C3AED", "#8B5CF6", "#A78BFA",
    "#C4B5FD", "#4F46E5", "#6366F1", "#818CF8",
    "#A5B4FC", "#C7D2FE"
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

    header[data-testid="stHeader"] {{
        background:{BG_MAIN} !important;
    }}

    div[data-testid="stToolbar"] {{
        background:{BG_MAIN} !important;
    }}

    section[data-testid="stSidebar"] {{
        background:{BG_CARD};
        border-right:1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color:{TEXT_MAIN} !important;
    }}

    div[data-testid="stMetric"] {{
        background:{BG_CARD};
        border:1px solid {BORDER};
        border-radius:16px;
        padding:18px;
    }}

    div[data-testid="stPlotlyChart"] {{
        background:{BG_CARD};
        border-radius:16px;
        border:1px solid {BORDER};
        padding:10px;
    }}

    .block-container {{
        padding-top:1.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# SHARED PLOTLY LAYOUT
# =====================================================

def style_fig(fig, y_title="", x_title="", show_legend=True):

    fig.update_layout(
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font_color=TEXT_MAIN,
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=show_legend,
        yaxis_gridcolor=GRID,
        xaxis_gridcolor=BG_CARD,
        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),
        margin=dict(t=20, l=10, r=10, b=10)
    )

    fig.update_xaxes(color=TEXT_MAIN)
    fig.update_yaxes(color=TEXT_MAIN)

    return fig

# =====================================================
# SMART DATA LOADER
# Local  -> SQL Server
# Cloud  -> CSV
# =====================================================

@st.cache_data(show_spinner=False)
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

        df = pd.read_sql(
            "SELECT * FROM enriched_orders",
            conn
        )

        conn.close()

    except Exception:

        BASE_DIR = Path(__file__).resolve().parents[2]
        csv_path = BASE_DIR / "data" / "enriched_orders.csv"

        df = pd.read_csv(csv_path)

    # ---------- Common Cleaning ----------

    for col in ["order_date", "expected_date", "actual_date"]:
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
