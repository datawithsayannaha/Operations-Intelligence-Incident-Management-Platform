import streamlit as st
import plotly.express as px
from views import common

def show(filtered):

    st.title("👥 Customer Intelligence")
    st.caption("Customer Analytics • Behavior • Segmentation")

    # =====================================================
    # CLEAN DATA
    # =====================================================

    df = filtered.copy()

    # Customer Segment
    df["customer_segment"] = (
        df["customer_segment"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "": "standard",
            "0": "standard",
            "std": "standard",
            "premium": "premium",
            "basic": "basic"
        })
        .map({
            "standard": "Standard",
            "premium": "Premium",
            "basic": "Basic"
        })
        .fillna("Standard")
    )

    # Region
    df["customer_region"] = (
        df["customer_region"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace({"": "Unknown", "nan": "Unknown", "None": "Unknown"})
        .str.title()
    )

    # =====================================================
    # KPI
    # =====================================================

    total_customers = df["customer_id"].nunique()
    total_orders = len(df)
    revenue = df["order_value"].sum()

    avg_customer_value = revenue / total_customers if total_customers else 0

    premium = (
        df["customer_segment"]
        .eq("Premium")
        .sum()
    )

    repeat_rate = (
        df.groupby("customer_id")
        .size()
        .ge(2)
        .mean() * 100
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("👤 Customers", f"{total_customers:,}")
    c2.metric("💰 Avg Customer Value", f"₹ {avg_customer_value:,.0f}")
    c3.metric("⭐ Premium Customers", f"{premium:,}")
    c4.metric("🔁 Repeat Rate", f"{repeat_rate:.1f}%")

    st.markdown("---")

    # =====================================================
    # ROW 1
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Customer Segment Distribution")

        seg = (
            df.groupby("customer_segment")
            .size()
            .reset_index(name="Customers")
        )

        fig = px.pie(
            seg,
            names="customer_segment",
            values="Customers",
            hole=0.62,
            color="customer_segment",
            color_discrete_map={
                "Standard": "#10B981",
                "Premium": "#3B82F6",
                "Basic": "#F59E0B"
            }
        )

        fig.update_traces(
            textfont_color=common.TEXT_MAIN,
            marker=dict(
                line=dict(color=common.BG_CARD, width=2)
            )
        )

        fig = common.style_fig(fig, show_legend=True)

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Customers by Region")

        region = (
            df.groupby("customer_region")["customer_id"]
            .nunique()
            .reset_index(name="Customers")
            .sort_values("Customers", ascending=False)
        )

        fig = px.bar(
            region,
            x="customer_region",
            y="Customers",
            color="customer_region",
            text_auto=True,
            color_discrete_sequence=common.REGION_PALETTE
        )

        fig.update_traces(
            marker_line_color="#0B1220",
            marker_line_width=1,
            textfont_color=common.TEXT_MAIN
        )

        fig = common.style_fig(
            fig,
            y_title="Customers",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # ROW 2
    # =====================================================

    left2, right2 = st.columns(2)

    with left2:

        st.subheader("🏆 Top 10 Customers")

        top = (
            df.groupby(["customer_id", "customer_name"])
            .agg(Revenue=("order_value", "sum"))
            .reset_index()
            .sort_values("Revenue", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top,
            x="Revenue",
            y="customer_name",
            orientation="h",
            color="Revenue",
            text_auto=".2s",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending")
        )

        fig = common.style_fig(
            fig,
            x_title="Revenue",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:

        st.subheader("Customer Lifetime Value")

        clv = (
            df.groupby("customer_id")
            .agg(
                Orders=("order_id", "count"),
                Revenue=("order_value", "sum")
            )
            .reset_index()
        )

        fig = px.scatter(
            clv,
            x="Orders",
            y="Revenue",
            size="Revenue",
            color="Revenue",
            color_continuous_scale="Viridis"
        )

        fig.update_layout(coloraxis_showscale=False)

        fig = common.style_fig(
            fig,
            x_title="Orders",
            y_title="Revenue",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================================
    # TABLE
    # =====================================================

    st.subheader("📋 Customer Summary")

    table = (
        df.groupby([
            "customer_id",
            "customer_name",
            "customer_segment",
            "customer_region"
        ])
        .agg(
            Total_Orders=("order_id", "count"),
            Revenue=("order_value", "sum"),
            Avg_Delay=("delivery_delay_days", "mean")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )