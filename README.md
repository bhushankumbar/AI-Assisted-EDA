# Superstore Sales Analytics Dashboard

An end-to-end exploratory data analysis solution for turning retail transaction data into decision-ready business insights. The project combines a filtered Streamlit dashboard, interactive Plotly visualizations, derived performance metrics, and an AI-assisted executive briefing.

## Project Scope

This analysis covers a 9,994-row, 21-column retail dataset and examines:

- Sales, profit, order volume, discount, and shipping KPIs
- Monthly sales and profit trends
- Regional, category, sub-category, and customer-segment performance
- Shipping-mode sales and profitability comparisons
- Discount distribution and its relationship to profit margin
- High-value products and loss-making transactions
- Data completeness, descriptive statistics, outliers, and distribution behavior
- Executive-level recommendations generated from computed analytical summaries

## What I Built

- Designed a reusable Pandas data preparation pipeline with date parsing and derived fields for shipping duration, profit margin, year, month, and sales bands.
- Built an interactive Streamlit dashboard with coordinated filters for date range, region, category, segment, and shipping mode.
- Developed Plotly visualizations for trend analysis, hierarchical category segmentation, shipping comparison, discount behavior, and distribution analysis.
- Added KPI calculations that update dynamically with the selected data slice.
- Implemented filtered dataset export for downstream analysis.
- Created an AI analysis engine that packages data quality checks, descriptive statistics, product profitability, sub-category performance, and shipping metrics into a structured Gemini executive briefing.

## Analytical Techniques

`Data cleaning` `Feature engineering` `Descriptive statistics` `GroupBy aggregation` `Time-series analysis` `KPI design` `Profitability analysis` `Outlier analysis` `Distribution analysis` `Interactive filtering` `Hierarchical segmentation` `AI-assisted insight generation`

## Technology

`Python` `Pandas` `Plotly Express` `Streamlit` `Google Gemini API`

## Project Architecture

```text
ai_eda_engine.py     Data profiling and AI executive briefing generation
eda_dashboard.py     Interactive dashboard and visualization layer
superstore_sales.csv Retail transaction dataset
charts/              Dashboard screenshots and analytical visualizations
```

## Dashboard Visuals

### Dashboard Overview and KPI Layer

![Dashboard overview with KPIs and filters](charts/img%201.png)

### Interactive Filter Panel

![Dashboard filter controls](charts/img%202.png)

### Monthly Profit Trend

![Monthly profit trend](charts/img%203.png)

### Category and Sub-Category Sales Treemap

![Category and sub-category sales treemap](charts/img%204.png)

### Average Sales and Profit by Shipping Mode

![Average sales and profit by shipping mode](charts/img%205.png)

### Profit Margin by Discount Range and Discount Distribution

![Profit margin by discount range and discount distribution](charts/img%206.png)

### AI Executive Insights Briefing

![AI-generated executive insights briefing](charts/img%207.png)

## Outcome

The project demonstrates how raw transactional data can be transformed into an analytical product that supports performance monitoring, profitability investigation, operational comparison, and concise executive communication.
