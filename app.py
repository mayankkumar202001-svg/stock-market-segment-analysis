import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

final=pd.read_csv("nifty_500_cleaned.csv")
final_df=pd.read_csv("nifty_500_cleaned.csv").pivot_table(index=["category","industry","company"],aggfunc="sum").reset_index().drop(["Unnamed: 0","book_value"], axis=1)

category_list=list(final_df["category"].unique())
industry_list=sorted(list(final_df["industry"].unique()))

st.sidebar.subheader("INDIAN STOCK MARKET")
category=st.sidebar.selectbox("Select category",category_list)
industry=st.sidebar.selectbox("Select industry",industry_list)
filtered_df = final_df[(final_df["industry"] == industry) & (final_df["category"] == category)]
company_list=sorted(list(filtered_df["company"].unique()))
company_list.insert(0,"OVER ALL ANALYSIS")
company=st.sidebar.selectbox("Select company",company_list)
btn=st.sidebar.button("DETAILS")

if company == "OVER ALL ANALYSIS":
    import streamlit as st
    import plotly.graph_objects as go

    # Assuming you already filtered your DataFrame into final_df

    # Create figure
    fig = go.Figure()

    # Bar for current stock value
    fig.add_trace(go.Bar(
        x=filtered_df['company'],
        y=filtered_df['current_value'],
        name='Current Value',
        marker_color='#38a7fc',
    ))

    # Line for 52-week low
    fig.add_trace(go.Scatter(
        x=filtered_df['company'],
        y=filtered_df['low_52week'],
        mode='lines+markers',
        name='52 Week Low',
        line=dict(color='red', dash='dot')
    ))

    # Line for 52-week high
    fig.add_trace(go.Scatter(
        x=filtered_df['company'],
        y=filtered_df['high_52week'],
        mode='lines+markers',
        name='52 Week High',
        line=dict(color='green', dash='dot')
    ))

    # Layout settings
    fig.update_layout(
        title='Stock Current Value with 52 Week High/Low',
        xaxis_title='Company',
        yaxis_title='Stock Price',
        barmode='group',
        xaxis_tickangle=-45
    )

    # Show in Streamlit
    st.plotly_chart(fig, use_container_width=True)


else:
    import streamlit as st
    import plotly.graph_objects as go

    # Pick a particular company
    company_name = company  # <-- change this dynamically if needed

    # Filter DataFrame for that company
    company_df = final_df[final_df["company"] == company_name]

    if not company_df.empty:
        # Select the row
        row = company_df.iloc[0]

        # Create dictionary of metrics
        metrics = {
            "Current Value": row["current_value"],
            "Dividend Yield": row["dividend_yield"],
            "52 Week High": row["high_52week"],
            "52 Week Low": row["low_52week"],
            "Market Cap": row["market_cap"],
            "Price/Earnings": row["price_earnings"],
            "ROCE": row["roce"],
            "ROE": row["roe"],
            "Sales Growth (3Y)": row["sales_growth_3yr"]
        }

        # Convert to Plotly table
        fig = go.Figure(data=[go.Table(
            header=dict(values=["Metric", "Value"],
                        fill_color="#02567a",
                        align="left"),
            cells=dict(values=[list(metrics.keys()), list(metrics.values())],
                       fill_color="#292b2b",
                       align="left"))
        ])

        fig.update_layout(title=f"Key Metrics for {company_name}")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"Company '{company_name}' not found in dataset")







