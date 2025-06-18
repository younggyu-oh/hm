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
