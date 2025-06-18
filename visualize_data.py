import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(
    page_title="HeyMax Growth Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connect
con = duckdb.connect("db/hm.duckdb")

# Load filter values
meta_df = con.execute("""
SELECT DISTINCT
  country,
  transaction_category
FROM s_active_users_d
""").fetchdf()

all_countries = sorted(meta_df["country"].unique())
all_categories = sorted(meta_df["transaction_category"].unique())

# ▶️ Title
st.title("📈 HeyMax Growth Metrics Dashboard")

# ▶️ Filter under title
st.markdown("### 🔍 Filters")
fcol1, fcol2 = st.columns(2)
with fcol1:
    selected_country = st.selectbox("Country", all_countries, index=all_countries.index('all'))
with fcol2:
    selected_category = st.selectbox("Transaction Category", all_categories, index=all_categories.index('all'))

def make_filter(field, value):
    return f"{field} = '{value}'"

where_clause = f"""
WHERE {make_filter('country', selected_country)} 
  AND {make_filter('transaction_category', selected_category)}
"""

# ▶️ Load DAU/WAU/MAU
dau_df = con.execute(f"""
SELECT dt AS activity_date, dau
FROM s_active_users_d
{where_clause}
ORDER BY dt
""").fetchdf()

wau_df = con.execute(f"""
SELECT week_start_date AS week, wau
FROM s_active_users_w
{where_clause}
ORDER BY week
""").fetchdf()

mau_df = con.execute(f"""
SELECT month_start_date AS month, mau
FROM s_active_users_m
{where_clause}
ORDER BY month
""").fetchdf()

# ▶️ DAU / WAU / MAU Line Charts
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👤 DAU")
    st.line_chart(dau_df.rename(columns={"activity_date": "Date"}).set_index("Date"), use_container_width=True)
with col2:
    st.subheader("📅 WAU")
    st.line_chart(wau_df.rename(columns={"week": "Week"}).set_index("Week"), use_container_width=True)
with col3:
    st.subheader("📆 MAU")
    st.line_chart(mau_df.rename(columns={"month": "Month"}).set_index("Month"), use_container_width=True)

# ▶️ Monthly Retention Table
monthly_retention_df = con.execute("""
SELECT
  month_start,
  new_user_count,
  retained_user_count,
  resurrected_user_count,
  churned_user_count
FROM s_user_retention_m
ORDER BY month_start DESC
""").fetchdf()

# ▶️ Monthly Retention Triangle
monthly_triangle_df = con.execute("""
SELECT
  cohort_month,
  month_offset,
  retention_rate,
  retained_users
FROM s_user_retention_triangle_m
ORDER BY cohort_month, month_offset
""").fetchdf()

monthly_triangle_pivot = monthly_triangle_df.pivot(index="cohort_month", columns="month_offset", values="retention_rate").fillna(0)
monthly_user_pivot = monthly_triangle_df.pivot(index="cohort_month", columns="month_offset", values="retained_users").fillna(0)

monthly_triangle_display_str = monthly_triangle_pivot.copy()
for i in monthly_triangle_pivot.index:
    for j in monthly_triangle_pivot.columns:
        rate = monthly_triangle_pivot.loc[i, j]
        count = int(monthly_user_pivot.loc[i, j])
        monthly_triangle_display_str.loc[i, j] = f"{rate:.0%} ({count})"

# ▶️ Display monthly retention
st.markdown("### 📆 Monthly Retention Table + Triangle Chart")
mcol1, mcol2 = st.columns([6, 4])
with mcol1:
    st.dataframe(monthly_retention_df, use_container_width=True)
with mcol2:
    st.dataframe(monthly_triangle_display_str, use_container_width=True)

# ▶️ Weekly Retention Table
weekly_retention_df = con.execute("""
SELECT
  week_start,
  new_user_count,
  retained_user_count,
  resurrected_user_count,
  churned_user_count
FROM s_user_retention_w
ORDER BY week_start DESC
""").fetchdf()

# ▶️ Weekly Retention Triangle
weekly_triangle_df = con.execute("""
SELECT
  cohort_week,
  week_offset,
  retention_rate,
  retained_users
FROM s_user_retention_triangle_w
ORDER BY cohort_week, week_offset
""").fetchdf()

weekly_triangle_pivot = weekly_triangle_df.pivot(index="cohort_week", columns="week_offset", values="retention_rate").fillna(0)
weekly_user_pivot = weekly_triangle_df.pivot(index="cohort_week", columns="week_offset", values="retained_users").fillna(0)

weekly_triangle_display_str = weekly_triangle_pivot.copy()
for i in weekly_triangle_pivot.index:
    for j in weekly_triangle_pivot.columns:
        rate = weekly_triangle_pivot.loc[i, j]
        count = int(weekly_user_pivot.loc[i, j])
        weekly_triangle_display_str.loc[i, j] = f"{rate:.0%} ({count})"

# ▶️ Display weekly retention
st.markdown("### 🗓️ Weekly Retention Table + Triangle Chart")
wcol1, wcol2 = st.columns([6, 4])
with wcol1:
    st.dataframe(weekly_retention_df, use_container_width=True)
with wcol2:
    st.dataframe(weekly_triangle_display_str, use_container_width=True)
