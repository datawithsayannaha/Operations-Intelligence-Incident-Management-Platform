import streamlit as st
import plotly.express as px
from views import common


def show(filtered):

    # =====================================================
    # CLEAN REGION NAMES
    # =====================================================

    df = filtered.copy()

    df["customer_region"] = (
        df["customer_region"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace({
            "": "Unknown",
            "nan": "Unknown",
            "None": "Unknown"
        })
        .str.title()
    )

    # =====================================================
    # HEADER
    # =====================================================

    st.title("📊 Operations Intelligence & Incident Management Platform")
    st.caption("Executive Dashboard")

    # =====================================================
    # KPI
    # =====================================================

    orders = len(df)
    revenue = df["order_value"].sum()

    delay_rate = (df["delivery_delay_days"] > 0).mean() * 100
    high_risk = (df["delivery_delay_days"] >= 5).sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Orders", f"{orders:,}")
    c2.metric("💰 Revenue", f"₹ {revenue/1_000_000:.2f} M")
    c3.metric("🚚 Delay Rate", f"{delay_rate:.1f}%")
    c4.metric("⚠️ High Risk", int(high_risk))

    st.markdown("---")

    # =====================================================
    # ROW 1
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Revenue by Region")

        reg = (
            df.groupby("customer_region")["order_value"]
            .sum()
            .reset_index()
            .sort_values("order_value", ascending=False)
        )

        fig = px.bar(
            reg,
            x="customer_region",
            y="order_value",
            text_auto=".2s",
            color="customer_region",
            color_discrete_sequence=common.REGION_PALETTE
        )

        fig.update_traces(
            marker_line_color="#0B1220",
            marker_line_width=1,
            textfont_color=common.TEXT_MAIN
        )

        fig = common.style_fig(
            fig,
            y_title="Revenue",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Orders by Status")

        status = (
            df.groupby("order_status")
            .size()
            .reset_index(name="Orders")
        )

        fig = px.pie(
            status,
            names="order_status",
            values="Orders",
            hole=0.60,
            color="order_status",
            color_discrete_map=common.STATUS_COLORS
        )

        fig.update_traces(
            textfont_color=common.TEXT_MAIN,
            marker=dict(
                line=dict(color=common.BG_CARD, width=2)
            )
        )

        fig = common.style_fig(
            fig,
            show_legend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # ROW 2
    # =====================================================

    left2, right2 = st.columns(2)

    with left2:

        st.subheader("Monthly Revenue")

        m = df.copy()

        m["Month"] = (
            m["order_date"]
            .dt.to_period("M")
            .astype(str)
        )

        m = (
            m.groupby("Month")["order_value"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            m,
            x="Month",
            y="order_value",
            markers=True
        )

        fig.update_traces(
            line_color=common.ACCENT_CYAN,
            marker_color="#38BDF8",
            line_width=3,
            marker_size=8
        )

        fig = common.style_fig(
            fig,
            y_title="Revenue",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:

        st.subheader("Top 10 Products")

        top = (
            df.groupby("product_id")["order_value"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        fig = px.bar(
            top,
            x="product_id",
            y="order_value",
            text_auto=".2s",
            color="product_id",
            color_discrete_sequence=common.PRODUCT_PALETTE
        )

        fig.update_traces(
            marker_line_color="#0B1220",
            marker_line_width=1,
            textfont_color=common.TEXT_MAIN
        )

        fig = common.style_fig(
            fig,
            y_title="Revenue",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================================
    # HIGH RISK
    # =====================================================

    st.subheader("⚠️ High Risk Orders")

    risk = df[df["delivery_delay_days"] >= 5][[
        "order_id",
        "customer_region",
        "product_id",
        "delivery_delay_days",
        "order_value"
    ]]

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # =====================================================
    # RAW DATA
    # =====================================================

    st.subheader("📋 Enriched Orders Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )