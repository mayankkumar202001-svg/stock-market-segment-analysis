import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
final = pd.read_csv("nifty_500_cleaned.csv")

# Create pivot table
final_df = (
    pd.read_csv("nifty_500_cleaned.csv")
    .pivot_table(index=["category", "industry", "company"], aggfunc="sum")
    .reset_index()
    .drop(["Unnamed: 0", "book_value"], axis=1)
)

# Sidebar filters
st.sidebar.subheader("📈 INDIAN STOCK MARKET")
category_list = list(final_df["category"].unique())
industry_list = sorted(list(final_df["industry"].unique()))

category = st.sidebar.selectbox("Select category", category_list)
industry = st.sidebar.selectbox("Select industry", industry_list)

filtered_df = final_df[
    (final_df["industry"] == industry) & (final_df["category"] == category)
]

company_list = sorted(list(filtered_df["company"].unique()))
company_list.insert(0, "OVER ALL ANALYSIS")

company = st.sidebar.selectbox("Select company", company_list)
btn = st.sidebar.button("DETAILS")

# ----------------- OVERALL ANALYSIS -----------------
if company == "OVER ALL ANALYSIS":
    fig = go.Figure()

    # Bar for current stock value
    fig.add_trace(
        go.Bar(
            x=filtered_df["company"],
            y=filtered_df["current_value"],
            name="Current Value",
            marker_color="#38a7fc",
        )
    )

    # Line for 52-week low
    fig.add_trace(
        go.Scatter(
            x=filtered_df["company"],
            y=filtered_df["low_52week"],
            mode="lines+markers",
            name="52 Week Low",
            line=dict(color="red", dash="dot"),
        )
    )

    # Line for 52-week high
    fig.add_trace(
        go.Scatter(
            x=filtered_df["company"],
            y=filtered_df["high_52week"],
            mode="lines+markers",
            name="52 Week High",
            line=dict(color="green", dash="dot"),
        )
    )

    # Layout settings
    fig.update_layout(
        title=dict(
            text="📊 Stock Current Value with 52 Week High/Low",
            font=dict(size=18),
            x=0.5,
            xanchor="center",
        ),
        xaxis_title="Company",
        yaxis_title="Stock Price",
        barmode="group",
        xaxis_tickangle=-45,
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------- COMPANY LEVEL ANALYSIS -----------------
else:
    company_name = company
    company_df = final_df[final_df["company"] == company_name]

    if not company_df.empty:
        row = company_df.iloc[0]

        # Create dictionary of metrics with formatting
        metrics = {
            "Current Value": f"₹{row['current_value']:,}",
            "Dividend Yield": f"{row['dividend_yield']:.2f}%",
            "52 Week High": f"₹{row['high_52week']:,}",
            "52 Week Low": f"₹{row['low_52week']:,}",
            "Market Cap": f"₹{row['market_cap'] / 1e7:.2f} Cr",
            "Price/Earnings": f"{row['price_earnings']:.2f}",
            "ROCE": f"{row['roce']:.2f}%",
            "ROE": f"{row['roe']:.2f}%",
            "Sales Growth (3Y)": f"{row['sales_growth_3yr']:.2f}%",
        }

        # Styled Plotly Table
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["<b>Metric</b>", "<b>Value</b>"],
                        fill_color="#02567a",
                        font=dict(color="white", size=14),
                        align=["left", "center"],
                        height=35,
                    ),
                    cells=dict(
                        values=[list(metrics.keys()), list(metrics.values())],
                        fill_color=[["#f9f9f9", "white"] * (len(metrics) // 2 + 1)],
                        align=["left", "center"],
                        font=dict(size=13),
                        height=30,
                    ),
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text=f"📊 Key Metrics for {company_name}",
                font=dict(size=18),
                x=0.5,
                xanchor="center",
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"Company '{company_name}' not found in dataset")
