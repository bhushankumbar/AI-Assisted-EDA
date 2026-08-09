# Superstore Sales EDA Project

This project performs end-to-end exploratory data analysis on the `superstore_sales.csv` dataset and exposes an interactive Streamlit dashboard along with an AI-powered executive summary.

## Project contents

- `ai_eda_engine.py` - Loads data, computes summary metrics, and generates an executive summary using Google Gemini.
- `eda_dashboard.py` - Interactive Streamlit dashboard for sales, profit, shipping, and category analytics.
- `superstore_sales.csv` - Retail transaction dataset.
- `requirements.txt` - Project dependencies.
- `.gitignore` - Keeps secrets and generated files out of source control.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini API key locally. Use one of these options:

   Option A - environment variable:
   ```bash
   setx GOOGLE_API_KEY "your_api_key_here"
   ```

   Option B - local key file:
   - create a file named `api_key.txt` in the project root
   - paste only your Gemini API key into that file

## Usage

### Generate AI executive summary

```bash
python ai_eda_engine.py
```

### Launch dashboard

```bash
streamlit run eda_dashboard.py
```

## Resume-worthy features

- Automated data profiling, KPI generation, and summary metrics.
- AI-guided executive insights generation using Gemini.
- Interactive dashboard with filtering, trend analysis, treemap segmentation, and profit/distribution visualizations.
- Downloadable filtered data export.
