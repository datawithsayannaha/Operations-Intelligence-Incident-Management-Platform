import streamlit as st
import requests
import pandas as pd
import json

# n8n Webhook
WEBHOOK_URL = "http://localhost:5678/webhook-test/operations-ai"


def show(filtered):

    st.title("🤖 AI Command Center")
    st.caption("Powered by n8n AI Agent")

    # ==========================
    # INPUT
    # ==========================

    question = st.text_area(
        "Ask Operations AI",
        placeholder="Which region generated the highest revenue?",
        height=140
    )

    # ==========================
    # ANALYZE
    # ==========================

    if st.button("🚀 Analyze", use_container_width=True):

        if not question.strip():
            st.warning("Please enter a business question.")
            return

        with st.spinner("AI Agent is analyzing live SQL data..."):

            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"question": question},
                    timeout=120
                )

                response.raise_for_status()
                data = response.json()

                answer = (
                    data.get("answer")
                    or data.get("output")
                    or data.get("response")
                    or data.get("text")
                )

                if answer is None:
                    st.error("No response received from n8n.")
                    st.json(data)
                    return

                # Convert JSON string → dict
                if isinstance(answer, str):
                    report = json.loads(answer)
                else:
                    report = answer

                # ==========================
                # EXECUTIVE REPORT
                # ==========================

                st.success("Analysis Complete")
                st.markdown("---")
                st.header("🧠 AI Executive Report")

                # Business Question
                st.subheader("❓ Business Question")
                st.info(report.get("user_question", question))

                # Executive Summary
                if report.get("executive_summary"):
                    st.subheader("📌 Executive Summary")
                    st.write(report["executive_summary"])

                # Problem
                if report.get("problem"):
                    st.subheader("🚨 Problem Identified")
                    st.error(report["problem"])

                # ==========================
                # Evidence
                # ==========================

                if report.get("evidence"):

                    st.subheader("📊 Evidence")
                    evidence_df = pd.DataFrame(report["evidence"])

                    # Customer report
                    if {
                        "rank",
                        "customer_id",
                        "customer_name",
                        "revenue"
                    }.issubset(evidence_df.columns):

                        evidence_df = evidence_df.rename(columns={
                            "rank": "Rank",
                            "customer_id": "Customer ID",
                            "customer_name": "Customer Name",
                            "revenue": "Revenue"
                        })

                        evidence_df["Revenue"] = evidence_df["Revenue"].apply(
                            lambda x: f"₹ {x:,.2f}"
                        )

                    # Product report
                    elif {
                        "rank",
                        "product_id",
                        "risk_score"
                    }.issubset(evidence_df.columns):

                        evidence_df = evidence_df.rename(columns={
                            "rank": "Rank",
                            "product_id": "Product ID",
                            "risk_score": "Risk Score"
                        })

                    # Carrier report
                    elif {
                        "rank",
                        "carrier",
                        "avg_delay_days"
                    }.issubset(evidence_df.columns):

                        evidence_df = evidence_df.rename(columns={
                            "rank": "Rank",
                            "carrier": "Carrier",
                            "avg_delay_days": "Avg Delay (Days)"
                        })

                    # Region report
                    elif {
                        "rank",
                        "region",
                        "revenue"
                    }.issubset(evidence_df.columns):

                        evidence_df = evidence_df.rename(columns={
                            "rank": "Rank",
                            "region": "Region",
                            "revenue": "Revenue"
                        })

                        evidence_df["Revenue"] = evidence_df["Revenue"].apply(
                            lambda x: f"₹ {x:,.2f}"
                        )

                    # Fallback metric/value
                    elif {
                        "metric",
                        "value"
                    }.issubset(evidence_df.columns):

                        evidence_df = evidence_df.rename(columns={
                            "metric": "Metric",
                            "value": "Value"
                        })

                    st.dataframe(
                        evidence_df,
                        use_container_width=True,
                        hide_index=True
                    )

                # Pattern
                if report.get("pattern"):
                    st.subheader("🔍 Pattern")
                    st.write(report["pattern"])

                # Root Cause
                if report.get("root_cause"):
                    st.subheader("🎯 Root Cause")
                    st.warning(report["root_cause"])

                # Business Impact
                if report.get("business_impact"):
                    st.subheader("💼 Business Impact")
                    st.write(report["business_impact"])

                # Recommendations
                actions = (
                    report.get("recommended_action")
                    or report.get("recommendation")
                )

                if actions:
                    st.subheader("✅ Recommended Actions")

                    for i, action in enumerate(actions, start=1):
                        st.markdown(f"**{i}.** {action}")

            except json.JSONDecodeError:
                st.error("AI returned invalid JSON.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to n8n. Check Docker & n8n.")

            except requests.exceptions.Timeout:
                st.error("Request timed out.")

            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP Error: {e}")

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

    # ==========================
    # Suggested Questions
    # ==========================

    st.markdown("---")
    st.subheader("💡 Suggested Questions")

    st.markdown("""
- Which region generated the highest revenue?
- Which carrier has the highest average delivery delay?
- Which products have the highest inventory risk?
- Where are we losing operational efficiency?
- Who are the top 10 customers by revenue?
""")

    # ==========================
    # System Status
    # ==========================

    st.markdown("---")
    st.subheader("🛰️ System Status")

    c1, c2, c3 = st.columns(3)

    c1.success("🟢 SQL Server")
    c2.success("🟢 Streamlit")
    c3.success("🟢 n8n AI Agent")