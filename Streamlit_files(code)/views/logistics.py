import streamlit as st
import plotly.express as px
from views import common


def show(filtered):

    st.title("🚚 Logistics Analytics")
    st.caption("Delivery Operations • Carrier Performance • Delay Intelligence")

    # =====================================================
    # CLEAN CARRIER NAMES
    # =====================================================

    df = filtered.copy()

    df["carrier"] = (
        df["carrier"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "": "unknown",
            "nan": "unknown",
            "none": "unknown",

            "fedex": "fedex",
            "fed ex": "fedex",

            "bluedart": "bluedart",
            "blue dart": "bluedart",

            "ecomexpress": "ecomexpress",
            "ecom express": "ecomexpress",

            "delhivery": "delhivery",
            "dhl": "dhl"
        })
    )

    df["carrier"] = df["carrier"].map({
        "fedex": "FedEx",
        "bluedart": "BlueDart",
        "ecomexpress": "EcomExpress",
        "delhivery": "Delhivery",
        "dhl": "DHL",
        "unknown": "Unknown"
    }).fillna("Unknown")

    # =====================================================
    # KPI
    # =====================================================

    delivered = (
        df["delivery_status"]
        .fillna("")
        .str.lower()
        .eq("delivered")
        .sum()
    )

    avg_delay = df["delivery_delay_days"].mean()

    delayed = (df["delivery_delay_days"] > 0).sum()

    on_time = (df["delivery_delay_days"] <= 0).sum()

    on_time_rate = (on_time / len(df)) * 100 if len(df) else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Delivered", f"{delivered:,}")
    c2.metric("⏱ Avg Delay", f"{avg_delay:.1f} Days")
    c3.metric("🚨 Delayed Orders", f"{delayed:,}")
    c4.metric("✅ On-Time Rate", f"{on_time_rate:.1f}%")

    st.markdown("---")

    # =====================================================
    # ROW 1
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Carrier Performance")

        carrier = (
            df.groupby("carrier")
            .agg(
                Orders=("order_id", "count"),
                Avg_Delay=("delivery_delay_days", "mean")
            )
            .reset_index()
            .sort_values("Orders", ascending=False)
        )

        fig = px.bar(
            carrier,
            x="carrier",
            y="Orders",
            color="Avg_Delay",
            text_auto=True,
            color_continuous_scale="RdYlGn_r"
        )

        fig.update_traces(
            marker_line_color="#0B1220",
            marker_line_width=1,
            textfont_color=common.TEXT_MAIN
        )

        fig.update_layout(coloraxis_colorbar_title="Days")

        fig = common.style_fig(
            fig,
            y_title="Orders",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Delivery Status")

        status = (
            df.groupby("delivery_status")
            .size()
            .reset_index(name="Orders")
        )

        fig = px.pie(
            status,
            names="delivery_status",
            values="Orders",
            hole=0.60,
            color="delivery_status",
            color_discrete_map={
                "Delivered": "#10B981",
                "In Transit": "#3B82F6",
                "Delayed": "#F59E0B",
                "Returned": "#EF4444"
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

    # =====================================================
    # ROW 2
    # =====================================================

    left2, right2 = st.columns(2)

    with left2:

        st.subheader("Delay Distribution")

        fig = px.histogram(
            df,
            x="delivery_delay_days",
            nbins=12,
            color_discrete_sequence=[common.ACCENT_CYAN]
        )

        fig = common.style_fig(
            fig,
            x_title="Delay (Days)",
            y_title="Orders",
            show_legend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:

        st.subheader("Delivery Cost vs Delay")

        scatter = df.dropna(
            subset=["delivery_cost", "delivery_delay_days"]
        )

        fig = px.scatter(
            scatter,
            x="delivery_cost",
            y="delivery_delay_days",
            size="order_value",
            color="carrier",
            color_discrete_sequence=common.REGION_PALETTE,
            hover_name="carrier"
        )

        fig = common.style_fig(
            fig,
            x_title="Delivery Cost",
            y_title="Delay (Days)",
            show_legend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================================
    # TABLE
    # =====================================================

    st.subheader("🚛 Carrier Performance Summary")

    table = (
        df.groupby("carrier")
        .agg(
            Orders=("order_id", "count"),
            Avg_Delay=("delivery_delay_days", "mean"),
            Avg_Cost=("delivery_cost", "mean"),
            Revenue=("order_value", "sum")
        )
        .reset_index()
        .sort_values("Orders", ascending=False)
    )

    table["Avg_Delay"] = table["Avg_Delay"].round(1)
    table["Avg_Cost"] = table["Avg_Cost"].round(2)
    table["Revenue"] = table["Revenue"].round(2)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )