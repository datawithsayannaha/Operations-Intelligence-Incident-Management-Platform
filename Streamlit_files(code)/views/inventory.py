import streamlit as st
import plotly.express as px
from views import common


def show(filtered):

    st.title("📦 Inventory Risk")
    st.caption("Stock Intelligence • Inventory Health • Product Risk")

    # =====================================================
    # CLEAN DATA
    # =====================================================

    df = filtered.copy()

    df["stock_available"] = (
        df["stock_available"]
        .fillna(0)
        .astype(int)
    )

    df["inventory_value"] = (
        df["stock_available"] * df["order_value"]
    )

    # =====================================================
    # KPI
    # =====================================================

    total_products = df["product_id"].nunique()
    total_stock = df["stock_available"].sum()

    low_stock = (
        df["stock_available"] <= 20
    ).sum()

    inventory_value = df["inventory_value"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Products", f"{total_products:,}")
    c2.metric("📊 Total Stock", f"{total_stock:,}")
    c3.metric("🚨 Low Stock", f"{low_stock:,}")
    c4.metric("💰 Inventory Value", f"₹ {inventory_value/1_000_000:.2f} M")

    st.markdown("---")

    # =====================================================
    # ROW 1
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Top 10 Inventory Value")

        inv = (
            df.groupby("product_id")
            .agg(Value=("inventory_value", "sum"))
            .reset_index()
            .sort_values("Value", ascending=False)
            .head(10)
        )

        fig = px.bar(
            inv,
            x="Value",
            y="product_id",
            orientation="h",
            color="Value",
            text_auto=".2s",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending")
        )

        fig = common.style_fig(
            fig,
            x_title="Inventory Value",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Stock Risk Distribution")

        risk = (
            df.groupby("product_id")
            .agg(Stock=("stock_available", "sum"))
            .reset_index()
        )

        risk["Risk"] = "Healthy"

        risk.loc[risk["Stock"] <= 3000, "Risk"] = "Critical"

        risk.loc[
            (risk["Stock"] > 3000) &
            (risk["Stock"] <= 8000),
            "Risk"
        ] = "Medium"

        risk = (
            risk.groupby("Risk")
            .size()
            .reset_index(name="Products")
        )

        fig = px.pie(
            risk,
            names="Risk",
            values="Products",
            hole=.60,
            color="Risk",
            color_discrete_map={
                "Healthy": "#10B981",
                "Medium": "#F59E0B",
                "Critical": "#EF4444"
            }
        )

        fig.update_traces(
            textfont_color=common.TEXT_MAIN,
            marker=dict(
                line=dict(
                    color=common.BG_CARD,
                    width=2
                )
            )
        )

        fig = common.style_fig(fig, show_legend=True)

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # ROW 2
    # =====================================================

    left2, right2 = st.columns(2)

    with left2:

        st.subheader("Fast Moving Products")

        fast = (
            df.groupby("product_id")
            .agg(Orders=("order_id", "count"))
            .reset_index()
            .sort_values("Orders", ascending=False)
            .head(10)
        )

        fig = px.bar(
            fast,
            x="product_id",
            y="Orders",
            color="Orders",
            text_auto=True,
            color_continuous_scale="Viridis"
        )

        fig.update_layout(coloraxis_showscale=False)

        fig = common.style_fig(
            fig,
            y_title="Orders",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:

        st.subheader("Stock vs Demand")

        demand = (
            df.groupby("product_id")
            .agg(
                Stock=("stock_available", "sum"),
                Orders=("order_id", "count"),
                Revenue=("order_value", "sum")
            )
            .reset_index()
        )

        fig = px.scatter(
            demand,
            x="Stock",
            y="Orders",
            size="Orders",
            color="Stock",
            hover_name="product_id",
            hover_data={
                "product_id": False,
                "Stock": ":,.0f",
                "Orders": True,
                "Revenue": ":,.0f"
            },
            color_continuous_scale="Turbo"
        )

        fig.update_layout(coloraxis_showscale=False)

        fig = common.style_fig(
            fig,
            x_title="Available Stock",
            y_title="Orders",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================================
    # TABLE
    # =====================================================

    st.subheader("📋 Inventory Summary")

    table = (
        df.groupby("product_id")
        .agg(
            Orders=("order_id", "count"),
            Stock=("stock_available", "sum"),
            Revenue=("order_value", "sum"),
            Avg_Delay=("delivery_delay_days", "mean")
        )
        .reset_index()
    )

    table["Risk"] = "Healthy"

    table.loc[table["Stock"] <= 3000, "Risk"] = "Critical"

    table.loc[
        (table["Stock"] > 3000) &
        (table["Stock"] <= 8000),
        "Risk"
    ] = "Medium"

    table = table.sort_values(
        ["Risk", "Stock", "Orders"],
        ascending=[True, True, False]
    )

    table["Revenue"] = table["Revenue"].round(2)
    table["Avg_Delay"] = table["Avg_Delay"].round(1)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )