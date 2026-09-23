# 🤖 Operations Intelligence & Incident Management Platform

> End-to-End AI-Powered Business Intelligence Platform using **Streamlit, n8n, SQL Server, Python & Groq LLM**

An enterprise-style Operations Intelligence platform that transforms natural language business questions into live SQL Server queries and generates executive-level operational reports using an AI Agent.

---

# 📌 Project Overview

This project simulates a real-world Operations Intelligence environment where business users can ask questions such as:

- Which region generated the highest revenue?
- Who are the top 10 customers by revenue?
- Which products have the highest inventory risk?
- Which carrier has the highest average delivery delay?
- Where are we losing operational efficiency?

The AI Agent automatically generates SQL, executes it on SQL Server, validates the result, and returns a structured executive report through Streamlit.

---

# 🏗️ Solution Architecture

```text
Business User
      │
      ▼
Streamlit Dashboard
      │
      ▼
n8n Webhook API
      │
      ▼
Main AI Agent
 ├───────────────┐
 │               │
 ▼               ▼
Groq LLM     SQL Tool
                  │
                  ▼
          SQL Server Database
                  │
                  ▼
        JSON Validation
                  │
                  ▼
      Executive Report
```

---

# ⚙️ Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Streamlit |
| Workflow Automation | n8n |
| Database | Microsoft SQL Server |
| Programming | Python |
| Data Processing | Pandas |
| LLM | Groq |
| Containerization | Docker |
| API | Webhook |

---

# 🔄 Workflow 1 — ETL & Data Quality Pipeline

## Objective

Design a production-style ETL pipeline that ingests multiple operational datasets, performs Python-based data cleaning and data quality validation, loads each dataset into Microsoft SQL Server, and builds a unified analytical table (`enriched_orders`) for downstream AI analytics.

---

## ETL Pipeline

```text
Orders.csv ───────────────┐
Customers.csv ────────────┤
Deliveries.csv ───────────┤
Support_Tickets.csv ──────┤
Inventory.csv ────────────┘
            │
            ▼
     Read Files from Disk
            │
            ▼
      Extract CSV Records
            │
            ▼
   Python Data Cleaning
            │
            ▼
   Data Quality Validation
            │
            ▼
   SQL Server Table Load
            │
            ├── Orders
            ├── Customers
            ├── Deliveries
            ├── Tickets
            └── Inventory
            │
            ▼
 SQL Join & Data Enrichment
            │
            ▼
     enriched_orders
            │
            ▼
 KPI Engine + AI Analytics
```

---

## Datasets

| Dataset | Rows |
|----------|-----:|
| Orders | 10,100 |
| Customers | 4,050 |
| Deliveries | 9,570 |
| Support Tickets | 5,060 |
| Inventory | 8,100 |

**Total Records Processed:** 36,880+

---

## Python Data Cleaning

Each dataset is cleaned independently using Python (Pandas).

- Missing value handling
- Duplicate removal
- Data type conversion
- Date standardization
- Payment status normalization
- Delivery status validation
- Inventory consistency checks
- Customer ID integrity validation

---

## Data Quality Engine

A dedicated DQ validation module evaluates every dataset before loading into SQL Server.

**Validation checks include:**

- Null value detection
- Duplicate records
- Invalid dates
- Negative quantities
- Invalid payment status
- Delivery delay validation
- Stock consistency rules

A consolidated **DQ Summary Report** is generated after all validations.

---

## SQL Server Data Warehouse

After successful validation, each cleaned dataset is loaded into its own SQL table.

| SQL Table | Source |
|-----------|--------|
| Orders | orders.csv |
| Customers | customers.csv |
| Deliveries | deliveries.csv |
| Tickets | support_tickets.csv |
| Inventory | inventory.csv |

Finally, SQL joins all operational tables to create the analytical table:

**`enriched_orders`**

This table becomes the single source of truth for KPI calculation and AI-driven business analysis.

---

## Output

- Clean SQL tables
- Data Quality Summary
- Unified `enriched_orders` analytical table
- Ready for KPI Engine & AI Agent
---

# 🤖 Workflow 2 — Conversational AI Agent

### Pipeline

```text
Chat Message
      │
      ▼
Main AI Agent
 ├───────────────┐
 │               │
 ▼               ▼
Groq Chat     SQL Tool
                  │
                  ▼
          Live SQL Query
                  │
                  ▼
        JSON Validator
                  │
                  ▼
 Business Rule Validator
                  │
                  ▼
   Executive Report Formatter
```

### AI Capabilities

- Natural Language to SQL
- Live SQL Execution
- Revenue Analytics
- Customer Analytics
- Inventory Risk Analysis
- Delivery Performance Analysis
- Root Cause Investigation
- Executive Report Generation

---

# 🌐 Workflow 3 — Streamlit Dashboard + Webhook API

### User Flow

```text
User Question
      │
      ▼
Streamlit UI
      │
      ▼
POST /webhook-test
      │
      ▼
n8n AI Agent
      │
      ▼
SQL Server
      │
      ▼
JSON Response
      │
      ▼
Executive Dashboard
```

### Dashboard Features

- AI Command Center
- Executive Summary
- Evidence Table
- Pattern Analysis
- Root Cause
- Business Impact
- Recommended Actions

---

# 📊 Database Schema

**Primary Table:** `enriched_orders`

| Category | Fields |
|----------|--------|
| Orders | order_id, order_date, quantity, order_value |
| Customer | customer_id, customer_name, customer_segment, customer_region |
| Product | product_id |
| Delivery | carrier, delivery_status, delivery_delay_days |
| Inventory | stock_available, reorder_level, daily_demand |
| Support | ticket_category, priority, sentiment |
| Finance | payment_status |

---

# 💡 Example Questions

```text
Which region generated the highest revenue?

Who are the top 10 customers by revenue?

Which products have the highest inventory risk?

Which carrier has the highest average delivery delay?

Where are we losing operational efficiency?
```

---

# 📈 Executive Report Structure

Every AI response is converted into a structured business report.

### Investigation Report

- Business Question
- Problem Identified
- Evidence
- Pattern
- Root Cause
- Business Impact
- Recommended Actions

### Analytical Report

- Business Question
- Executive Summary
- Evidence
- Business Impact
- Recommended Actions

---

# ✨ Key Features

- ✅ Natural Language SQL Generation
- ✅ Live SQL Server Query Execution
- ✅ AI Business Analyst
- ✅ Executive Report Generator
- ✅ KPI Investigation Engine
- ✅ Data Quality Validation
- ✅ Streamlit Dashboard
- ✅ REST Webhook API
- ✅ Docker Self-hosted Deployment

---

# 📁 Repository Structure

```text
Operations-Intelligence-Incident-Management-Platform
│
├── app.py
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── workflows/
│   ├── etl_workflow.json
│   ├── ai_chat_workflow.json
│   └── webhook_workflow.json
│
├── datasets/
│   ├── orders.csv
│   ├── customers.csv
│   ├── deliveries.csv
│   ├── tickets.csv
│   └── inventory.csv
│
├── screenshots/
│   ├── dashboard.png
│   ├── etl_workflow.png
│   ├── ai_agent.png
│   └── executive_report.png
│
└── sql/
    └── enriched_orders_schema.sql
```

---

# 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/datawithsayannaha/Operations-Intelligence-Incident-Management-Platform.git
cd Operations-Intelligence-Incident-Management-Platform
```

### Start Docker

```bash
docker compose up -d
```

### Run Streamlit

```bash
streamlit run app.py
```

### Open Dashboard

```text
http://localhost:8501
```

---

# 📸 Screenshots

Add the following screenshots inside the **/screenshots** folder:

- ETL Workflow
- AI Agent Workflow
- Streamlit Dashboard
- Executive Report
- SQL Query Results

---

# 👨‍💻 Author

**Sayan Naha**

Data Analyst • SQL • Python • Power BI • Microsoft Fabric • AI Automation

GitHub: **@datawithsayannaha**

---

## ⭐ Star this repository if you found it useful!
