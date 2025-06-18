# HM Growth Analytics

## Overview

The goal is to construct an end-to-end analytics stack that loads user events and enables tracking of growth metrics such as Daily/Weekly/Monthly Active Users and Retention.

---

## Technologies Used

* **DuckDB**: Lightweight analytical database used for local querying.
* **Streamlit**: Interactive web UI for dashboarding.
* **Python (pandas, duckdb)**: For ETL and transformation logic.

> ⚠️ These tools were selected solely for the purpose of the assignment. In a production environment, different tech stacks would be more appropriate. Please refer to the "DW Design Proposal" section below for more realistic stack considerations.

---

## 🚀 How to Run

### 🔗 Live Dashboard

> Streamlit public URL: *\[https://hm-younggyu-oh.streamlit.app/]*

### 🖥️ Local Setup

```bash
# Clone the repo
$ git clone https://github.com/younggyu-oh/hm.git
$ cd hm

# (Optional) create virtual env
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

# Run Streamlit
$ streamlit run Step2-visualize_data.py
```

