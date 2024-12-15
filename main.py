import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
data = pd.read_csv('data.csv', parse_dates=['Order Date', 'Ship Date'], encoding='latin1')

# Add title and description
st.title("Superstore Sales Dashboard")
st.markdown("""
This dashboard provides insights into sales, profit, and product performance.
Navigate through the tabs for detailed visualizations!
""")

# Sidebar Filters
st.sidebar.header("Filter Data")
regions = st.sidebar.multiselect("Select Region(s):", options=data['Region'].unique(), default=data['Region'].unique())
categories = st.sidebar.multiselect("Select Category(ies):", options=data['Category'].unique(), default=data['Category'].unique())

# Apply Filters
filtered_data = data[(data['Region'].isin(regions)) & (data['Category'].isin(categories))]

# Total Sales, Profit, and Quantity
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
total_quantity = filtered_data['Quantity'].sum()

# KPI Metrics
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity", f"{total_quantity:,}")

# Monthly Sales Trend
filtered_data['Order Month'] = filtered_data['Order Date'].dt.to_period('M')
monthly_sales = filtered_data.groupby('Order Month')['Sales'].sum().reset_index()
monthly_sales['Order Month'] = monthly_sales['Order Month'].astype(str)

st.subheader("Monthly Sales Trend")
fig = px.line(monthly_sales, x='Order Month', y='Sales', title='Sales Over Time', markers=True)
st.plotly_chart(fig)

# Sales by Region
st.subheader("Sales by Region")
region_sales = filtered_data.groupby('Region')['Sales'].sum().reset_index()
fig = px.bar(region_sales, x='Region', y='Sales', title='Regional Sales', text_auto='.2s', color='Region')
st.plotly_chart(fig)

# Top 10 Products by Sales
st.subheader("Top 10 Products by Sales")
top_products = filtered_data.groupby('Product Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
fig = px.bar(top_products, x='Sales', y='Product Name', orientation='h', title='Top 10 Products', text_auto='.2s', color='Sales')
st.plotly_chart(fig)

# Sales by Category and Sub-Category
st.subheader("Sales by Category and Sub-Category")
category_sales = filtered_data.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
fig = px.sunburst(category_sales, path=['Category', 'Sub-Category'], values='Sales', title='Category Performance')
st.plotly_chart(fig)
