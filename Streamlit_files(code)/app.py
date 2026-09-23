import streamlit as st
from views import common, executive, customer, logistics, inventory, ai_command

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Operations Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Theme
common.inject_theme()

# =====================================================
# LOAD DATA
# =====================================================

df = common.load_data()

# Merge Blank + Unknown Region
df["customer_region"] = (
    df["customer_region"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .replace("", "Unknown")
    .str.title()
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("# 📊 OIM Platform")
st.sidebar.caption("Operations Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Customer Intelligence",
        "Logistics Analytics",
        "Inventory Risk",
        "AI Command Center"
    ]
)

st.sidebar.markdown("---")

regions = ["All"] + sorted(df["customer_region"].unique().tolist())

region = st.sidebar.selectbox(
    "🌍 Region Filter",
    regions
)

st.sidebar.markdown("---")
st.sidebar.success("🟢 SQL Server Connected")

# =====================================================
# FILTER
# =====================================================

if region == "All":
    filtered = df.copy()
else:
    filtered = df[df["customer_region"] == region]

# =====================================================
# PAGE DISPATCH
# =====================================================

if page == "Executive Dashboard":
    executive.show(filtered)

elif page == "Customer Intelligence":
    customer.show(filtered)

elif page == "Logistics Analytics":
    logistics.show(filtered)

elif page == "Inventory Risk":
    inventory.show(filtered)

elif page == "AI Command Center":
    ai_command.show(filtered)