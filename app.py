import streamlit as st
import pandas as pd
import plotly.express as px

def run(df: pd.DataFrame):
    st.title("My Company Analyst Dashboard")
    total_sales = (
        df[df['Status'] == 'Completed']
        .groupby([df['OrderDate'].dt.year.rename('Year'), df['OrderDate'].dt.month.rename('Month')])
        .size()
        .reset_index(name='TotalSales')
    )
    years_ls = total_sales['Year'].unique().tolist()
    selected_years = st.multiselect(
        'Filter by year:',
        options=years_ls,
        default=years_ls
    )

    yearly_sales = (total_sales.groupby('Year', as_index=False)['TotalSales'].sum())
    filtered_yearly_sales = yearly_sales[yearly_sales['Year'].isin(selected_years)]
    fig = px.bar(
        filtered_yearly_sales,
        width=200,
        height=600,
        x='Year',
        y='TotalSales',
        title='Total Sales Over Year',
        text_auto=True
    )

    st.plotly_chart(fig)

    filtered_total_sales = total_sales[total_sales['Year'].isin(selected_years)]
    fig = px.line(
        filtered_total_sales,
        x='Month',
        y='TotalSales',
        color='Year',
        title='Line chart Total Sales Over Year',
        line_shape='spline'
    )

    st.plotly_chart(fig)