# HM Growth Analytics

## Project Overview

The goal is to construct an end-to-end analytics stack that loads user events and enables tracking of growth metrics such as Daily/Weekly/Monthly Active Users and Retention.

---

## Technologies Used

* **Database**: `DuckDB` 
* **Transformation & Modeling**: `dbt` 
* **Visualization**: `Streamlit` 
* **ETL/Execution Engine**: `Python` 

> These tools were selected solely for the purpose of this exercise. In a production environment, different tooling would be more appropriate. Please refer to the "DW System Design" section below for more realistic stack considerations.

---

## Project Directory Structure

```text
├── data/                
│   └── event_stream.csv        # Raw input data (event logs)
├── db/                  
│   └── hm.duckdb               # DuckDB file (used as warehouse)
├── hm_analytics/        
│   └── models/                
│       ├── dm/                 # Data Marts (summary models for dashboard use)
│       └── dw/                 # Core DW tables (dim, fact layer)
├── load_data_to_duckdb.py      # Initial loader script for raw CSV -> DuckDB
├── visualize_data.py           # Streamlit app for dashboard rendering
├── setup.sh                    # One-click setup script (env, install, dbt, data load)
├── requirements.txt            # Python dependency list
└── README.md                   # Project documentation
```

---

## How to Run

### Live Dashboard

> public URL: *\[https://younggyu-oh.streamlit.app/]*

### Local Setup
```bash
# 0. (Optional) Ensure Python 3.10+ is installed
$ python3 --version
# If needed, install via pyenv or system package manager

# 1. Clone the repo
$ git clone https://github.com/younggyu-oh/hm.git
$ cd hm

# 2. Run the full setup script
$ chmod +x setup.sh
$ ./setup.sh
```

---

## Dashboard Features


* **Metrics Visualized**:

  * Daily / Weekly / Monthly Active Users (DAU, WAU, MAU)
    * Filters: `Country`, `Transaction Category` 
  * Growth Accounting: New, Retained, Resurrected, Churned Users
  * Retention Triangle: Weekly + Monthly

---

## Data Warehouse Tables & Lineage

### Source Table

* `raw_events_d`: Raw user event logs

### Data Warehouse Layer (Fact & Dimension)

* `fct_events_d`: Cleaned and enriched user event logs for analytics
* `dim_users`: User profile and signup metadata
* `dim_date`: Date dimension for time-based joins and calendar aggregations

### Data Mart Layer (Summary)

* `s_active_users_d/w/m`: Active user counts by day/week/month
* `s_user_total_activity_d`: Each user's first/last event and cumulative stats
* `s_user_activity_w/m`: Weekly and monthly per-user activity summaries
* `s_user_retention_w/m`: Growth accounting classification (new, retained, churned, resurrected)
* `s_user_retention_triangle_w/m`: Cohort-based triangle retention views

### Lineage Diagram

```text
raw_events_d
  └──► fct_events_d
        ├──► s_active_users_d/w/m
        ├──► s_user_total_activity_d
        └──► s_user_activity_w/m

s_user_total_activity_d, s_user_activity_w/m
  ├──► s_user_retention_w/m
  └──► s_user_retention_triangle_w/m

(dim_users, dim_date used across joins)
```

### DW Modeling Notes

* A clear separation between DW and DM layers helps ensure scalability and clarity.
* Pre-aggregating user-level and period-level activity allows for efficient retention metric computation, avoiding full-table scans and reducing memory usage.

---

## DW System Design

### Traffic Estimation

| Metric                         | Estimate                            |
| ------------------------------ | ----------------------------------- |
| Registered Users               | 200,000                             |
| Monthly Active Users (MAU)     | 50,000                              |
| Daily Active Users (DAU)       | 10,000                              |
| Estimated Daily Event Volume   | 20MB (10000 X 10events X 200bytes)  |
| Estimated Monthly Event Volume | 600MB                               |

---

### Current Stack 

* **Storage**: Google BigQuery 
* **Modeling**: dbt 
* **Visualization**: Superset
* **Event Tracking**: Mixpanel 

---

### Stack Recommendations by Layer

| Layer                      | Options                                  | Recommendation & Notes                                                                               |
| -------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Storage (Data Lake)**    | GCS (with Parquet), BigQuery             | Use GCS + Parquet for flexibility across compute layers (BigQuery, Spark, etc.)                      |
| **Compute / Query Engine** | BigQuery, Spark(Databricks), Trino       | BigQuery will likely remain the main query engine. Spark enables scalable parallel processing. if query volume grows and BigQuery costs rise, consider moving heavy workloads to dedicated compute with Trino.  |
| **Transformation**         | dbt                                      | Keep using dbt                                                                                       |
| **Batch Orchestration**    | Airflow                                  | Airflow is mature and Google-friendly                                                                |
| **Real-time Processing**   | Kafka + Flink / Spark Streaming          | If needed for real-time feeds. otherwise batch should suffice early on                               |
| **Real-time Storage**      | Bigtable, Redis, Firestore               | Only if real-time serving (e.g., feature store or dashboard APIs) becomes essential. (expensive)     |
| **BI / Visualization**     | Superset, Looker                         | Superset is good for simple analysis. Looker for scalable governance later                           |
| **Data Quality & Testing** | dbt tests, Great Expectations            | Add dbt tests and layer on Great Expectations for critical flows                                     |


 




