import os
import pandas as pd
from google import genai

DATASET_PATH = "superstore_sales.csv"
OUTPUT_PATH = "ai_executive_summary.md"
API_KEY_FILE = "api_key.txt"


def load_dataset(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path, encoding="windows-1252")
    except Exception:
        return pd.read_csv(path)


def read_api_key_from_file(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip() or None


def get_api_key() -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key.strip()

    api_key = read_api_key_from_file(API_KEY_FILE)
    if api_key:
        return api_key

    raise RuntimeError(
        "Gemini API key not found. Set GOOGLE_API_KEY or create api_key.txt with your key."
    )


def build_prompt(data_shape: str, missing_values: str, descriptive_stats: str, top_products_by_profit: str, sub_category_performance: str, shipping_mode_impact: str) -> str:
    return f"""
You are an expert Lead Data Analyst reviewing enterprise transaction records.
Analyze the following dataset summaries and output a highly structured executive data briefing.

DATASET DIMENSIONS:
{data_shape}

DATA QUALITY & MISSING VALUES TRACKING:
{missing_values}

OVERALL DESCRIPTIVE STATISTICS:
{descriptive_stats}

TOP 5 PROFIT-GENERATING PRODUCTS:
{top_products_by_profit}

SUB-CATEGORY SALES & PROFIT METRICS:
{sub_category_performance}

SHIPPING MODE PROFITABILITY & DISCOUNT RELATIONSHIPS:
{shipping_mode_impact}

Provide your response in perfectly formatted Markdown with these exact sections:
# EXECUTIVE INSIGHTS BRIEFING

## 1. Data Integrity & Quality Issues
(Flag serious missing data chunks, data types, or distribution skew challenges)

## 2. Top 3 Hidden Revenue/Profit Drivers
(Identify specific statistical interactions or performance clusters standard queries miss)

## 3. Immediate Algorithmic Action Plan for Stakeholders
(Provide a step-by-step business strategy backed directly by the data columns)
"""


def summarize_dataset(df: pd.DataFrame) -> tuple[str, str, str, str, str, str]:
    data_shape = f"Rows: {df.shape[0]}, Columns: {df.shape[1]}"
    missing_values = df.isnull().sum().to_string()
    descriptive_stats = df.describe(include="all").to_string()
    top_products_by_profit = df.groupby("Product Name")["Profit"].sum().nlargest(5).to_string()
    sub_category_performance = df.groupby("Sub-Category")[["Sales", "Profit"]].sum().to_string()
    shipping_mode_impact = df.groupby("Ship Mode")[["Profit", "Discount"]].mean().to_string()
    return (
        data_shape,
        missing_values,
        descriptive_stats,
        top_products_by_profit,
        sub_category_performance,
        shipping_mode_impact,
    )


def generate_summary(prompt: str, api_key: str) -> str:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = getattr(response, "text", None)
        if text:
            return text

        candidates = getattr(response, "candidates", None)
        if candidates:
            first = candidates[0]
            return getattr(first, "content", None) or getattr(first, "text", None) or str(first)

        return response.json()
    except Exception as exc:
        raise RuntimeError(
            f"AI Summary generation failed: {exc}.\nEnsure your Gemini API key is valid and network access is available."
        )


def main() -> None:
    df = load_dataset(DATASET_PATH)
    print("Starting data matrix calculations...")

    (
        data_shape,
        missing_values,
        descriptive_stats,
        top_products_by_profit,
        sub_category_performance,
        shipping_mode_impact,
    ) = summarize_dataset(df)

    print("Structural metrics computed. Packaging payload...")
    prompt = build_prompt(
        data_shape,
        missing_values,
        descriptive_stats,
        top_products_by_profit,
        sub_category_performance,
        shipping_mode_impact,
    )

    api_key = get_api_key()
    print("Sending metrics payload to Gemini API...")

    summary_text = generate_summary(prompt, api_key)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print("Execution finished successfully. Output files updated.")


if __name__ == "__main__":
    main()
