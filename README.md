# Superstore Sales Analytics Dashboard

An end-to-end exploratory data analysis project that transforms retail transaction data into an interactive analytics dashboard and an AI-assisted executive briefing.

The application helps stakeholders explore sales, profitability, discounts, shipping performance, and product category trends through interactive filters and visualizations. A separate analysis engine uses Google Gemini to convert calculated dataset insights into a structured executive summary.

## Highlights

- Interactive Streamlit dashboard for retail performance analysis
- KPI tracking for sales, profit, orders, discount, and shipping time
- Date, region, category, segment, and shipping-mode filters
- Monthly sales and profit trend analysis
- Category and sub-category sales treemap
- Shipping-mode comparison and discount distribution analysis
- Profit-margin analysis across discount ranges
- Export of filtered data as CSV
- AI-generated executive insights based on computed data summaries

## Technology Stack

- **Python** for data processing and application logic
- **Pandas** for data cleaning, transformation, and aggregation
- **Plotly Express** for interactive visualizations
- **Streamlit** for the web dashboard
- **Google Gemini API** for the optional executive summary

## Project Structure

```text
.
├── ai_eda_engine.py          # Computes metrics and generates the AI briefing
├── eda_dashboard.py          # Streamlit dashboard application
├── superstore_sales.csv      # Retail transaction dataset
├── charts/                   # Dashboard visualization previews
├── requirements.txt          # Python dependencies
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/bhushankumbar/AI-Assisted-EDA.git
cd AI-Assisted-EDA
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run eda_dashboard.py
```

Streamlit will provide a local URL, normally `http://localhost:8501`.

## Optional AI Executive Summary

The dashboard can display `ai_executive_summary.md` when the file has been generated. To create or refresh it, configure a Gemini API key using either method below.

### Environment variable

PowerShell:

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

### Local key file

Create `api_key.txt` in the project root and add only the API key. This file is excluded from Git by `.gitignore`.

Then run:

```bash
python ai_eda_engine.py
```

The generated summary is saved locally as `ai_executive_summary.md`.

## Dashboard Preview

![Sales trend visualization](charts/img%201.png)

![Profit analysis visualization](charts/img%202.png)

![Category performance visualization](charts/img%203.png)

## Data Workflow

1. Load and parse transaction data from the CSV dataset.
2. Derive order dates, shipping duration, profit margin, year, month, and sales category fields.
3. Apply user-selected dashboard filters.
4. Calculate filtered KPIs and render interactive visualizations.
5. Optionally summarize the dataset with Google Gemini for executive-level insights.

## Security Note

API keys are kept out of source control through `.gitignore`. Never commit credentials, tokens, or other private configuration files to the repository.
