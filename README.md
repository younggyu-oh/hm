# HM Growth Analytics

## Project Overview

The goal is to construct an end-to-end analytics stack that loads user events and enables tracking of growth metrics such as Daily/Weekly/Monthly Active Users and Retention.

---

## Technologies Used

* **Database**: `DuckDB` – Used for fast, in-process analytical querying and storing transformed event/user data.
* **Transformation & Modeling**: `dbt` – Used for SQL-based data modeling and creation of core tables (`dim_users`, `fct_events`, etc.).
* **Visualization**: `Streamlit` – Used to build the interactive dashboard with filters and metric visualizations.
* **ETL/Execution Engine**: `Python` – Used for orchestrating data load and transformation using `pandas` and executing SQL via `duckdb`.

> These tools were selected solely for the purpose of this exercise. In a production environment, different tooling would be more appropriate. Please refer to the "DW Design Proposal" section below for more realistic stack considerations.

---

## How to Run

### Live Dashboard

> public URL: *\[https://hm-younggyu-oh.streamlit.app/]*

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

* **Filters**: `Country`, `Transaction Category`
* **Metrics Visualized**:

  * Daily / Weekly / Monthly Active Users (DAU, WAU, MAU)
  * Growth Accounting: New, Retained, Resurrected, Churned Users
  * Retention Triangle: Weekly + Monthly

---

## 🧱 Data Warehouse Tables & Lineage

### 🗃️ Source Table

* `raw_events_d`: Raw user event logs

### 🧩 Data Warehouse Layer (Fact & Dimension)

* `fct_events_d`: Cleaned and enriched user event logs for analytics
* `dim_users`: User profile and signup metadata
* `dim_date`: Date dimension for time-based joins and calendar aggregations

### 📊 Data Mart Layer (Summary)

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
  └──► s_user_retention_w/m
       └──► s_user_retention_triangle_w/m

(dim_users, dim_date used across joins)
```

### DW Modeling Notes

* A clear separation between DW and DM layers helps ensure scalability and clarity.
* Pre-aggregating user-level and period-level activity allows for efficient retention metric computation, avoiding full-table scans and reducing memory usage.

