import pathlib

import pandas as pd
import plotly.express as px
import streamlit as st

DATASET_PATH = pathlib.Path("superstore_sales.csv")
AI_SUMMARY_PATH = pathlib.Path("ai_executive_summary.md")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH, encoding="windows-1252")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin"] = df["Profit"] / df["Sales"].replace({0: pd.NA})
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Sales Category"] = pd.cut(
        df["Sales"],
        bins=[-1, 50, 200, 500, 2000, df["Sales"].max()],
        labels=["Very Low", "Low", "Medium", "High", "Very High"],
    )
    return df


def filter_data(
    df: pd.DataFrame,
    date_range: tuple,
    regions: list[str],
    categories: list[str],
    segments: list[str],
    ship_modes: list[str],
) -> pd.DataFrame:
    if date_range:
        start_date, end_date = date_range
        df = df[(df["Order Date"] >= pd.to_datetime(start_date)) & (df["Order Date"] <= pd.to_datetime(end_date))]
    if regions:
        df = df[df["Region"].isin(regions)]
    if categories:
        df = df[df["Category"].isin(categories)]
    if segments:
        df = df[df["Segment"].isin(segments)]
    if ship_modes:
        df = df[df["Ship Mode"].isin(ship_modes)]
    return df


def show_kpis(df: pd.DataFrame) -> None:
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    avg_discount = df["Discount"].mean()
    avg_days_to_ship = df["Days to Ship"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Avg. Discount", f"{avg_discount:.1%}")
    col5.metric("Avg. Days to Ship", f"{avg_days_to_ship:.1f}")


def show_charts(df: pd.DataFrame) -> None:
    sales_trend = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
    fig_sales = px.line(sales_trend, x="Month", y="Sales", title="Sales Trend by Month", markers=True)
    fig_profit = px.line(sales_trend, x="Month", y="Profit", title="Profit Trend by Month", markers=True)

    category_profit = (
        df.groupby(["Category", "Sub-Category"])[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    fig_treemap = px.treemap(
        category_profit,
        path=["Category", "Sub-Category"],
        values="Sales",
        color="Profit",
        title="Category & Sub-Category Sales Treemap",
        color_continuous_scale="RdYlGn",
    )

    ship_mode = df.groupby("Ship Mode")[["Profit", "Sales"]].mean().reset_index()
    fig_ship = px.bar(
        ship_mode,
        x="Ship Mode",
        y=["Sales", "Profit"],
        barmode="group",
        title="Average Sales and Profit by Ship Mode",
    )

    discount_bins = pd.cut(
        df["Discount"],
        bins=[-0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0],
        labels=["0-5%", "5-10%", "10-20%", "20-30%", "30-50%", "50%+"],
    )
    discount_profit = (
        df.assign(DiscountRange=discount_bins)
        .groupby("DiscountRange")["Profit Margin"]
        .mean()
        .reset_index()
    )
    fig_profit_margin = px.bar(
        discount_profit,
        x="DiscountRange",
        y="Profit Margin",
        title="Average Profit Margin by Discount Range",
        labels={"DiscountRange": "Discount Range", "Profit Margin": "Avg Profit Margin"},
        text=discount_profit["Profit Margin"].map(lambda x: f"{x:.1%}"),
    )
    fig_profit_margin.update_traces(textposition="outside")

    fig_discount = px.histogram(df, x="Discount", nbins=20, title="Discount Distribution")

    st.plotly_chart(fig_sales, use_container_width=True)
    st.plotly_chart(fig_profit, use_container_width=True)
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.plotly_chart(fig_ship, use_container_width=True)
    st.plotly_chart(fig_profit_margin, use_container_width=True)
    st.plotly_chart(fig_discount, use_container_width=True)


def show_ai_summary() -> None:
    if AI_SUMMARY_PATH.exists():
        st.header("AI Executive Summary")
        text = AI_SUMMARY_PATH.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        preview = "\n".join(lines[:8])
        st.markdown(preview)
        if len(lines) > 8:
            with st.expander("Show full AI summary"):
                st.markdown("\n".join(lines[8:]))
    else:
        st.info("The AI executive summary will appear here after the summary file is created or refreshed.")


def main() -> None:
    st.set_page_config(page_title="Superstore Sales EDA Dashboard", page_icon="📊", layout="wide")
    st.markdown(
        """
        <div style='display:flex; justify-content:space-between; align-items:flex-end; width:100%;'>
            <div>
                <h1 style='margin:0; font-size:2.6rem;'>Superstore Sales EDA Dashboard</h1>
                <p style='margin:0; color:#9aa5b1; font-size:1.05rem;'>AI-driven retail analytics for sales, profit, shipping, and category performance.</p>
            </div>
            <div style='text-align:right; color:#9aa5b1;'>
                <p style='margin:0;'>Enterprise retail dataset</p>
                <p style='margin:0;'>Modern EDA & executive briefing</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.sidebar.header("Filters")
    st.sidebar.markdown(
        "Use the controls below to narrow the dataset by order date, region, product category, customer segment, and shipping mode."
    )
    st.sidebar.caption(
        "AI summary content is refreshed whenever the summary file is updated."
    )

    df = load_data()
    date_min = df["Order Date"].min().date()
    date_max = df["Order Date"].max().date()
    selected_dates = st.sidebar.date_input("Order Date range", [date_min, date_max])

    regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    segments = st.sidebar.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
    ship_modes = st.sidebar.multiselect("Ship Mode", sorted(df["Ship Mode"].unique()), default=sorted(df["Ship Mode"].unique()))

    filtered_df = filter_data(df, tuple(selected_dates), regions, categories, segments, ship_modes)

    if filtered_df.empty:
        st.warning("No records match the selected filters. Adjust the filter selection to see the dashboard.")
        return

    show_kpis(filtered_df)

    st.markdown("---")
    st.subheader("Performance Trends")
    show_charts(filtered_df)

    st.markdown("---")
    st.subheader("Filtered Dataset Preview")
    st.dataframe(filtered_df.head(20), use_container_width=True)

    st.markdown("---")
    show_ai_summary()

    with st.expander("Download filtered dataset"):
        st.download_button(
            label="Export CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="superstore_filtered.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
