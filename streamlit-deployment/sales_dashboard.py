import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Superstore Sales Dashboard", 
    layout="wide",
    page_icon="📊"
)

# Title and description
st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive dashboard for analyzing sales performance across regions, categories, and time periods.")

# Load data function with caching
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Dataset/Processed/cleaned_sales_data.csv')
        # Convert date columns if needed
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except FileNotFoundError:
        st.error("❌ cleaned_sales_data.csv not found. Please run your analysis notebook first.")
        return None

# Load data
df = load_data()

if df is None:
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
if 'Order Date' in df.columns:
    min_date = df['Order Date'].min()
    max_date = df['Order Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Region filter
selected_region = st.sidebar.multiselect(
    "Select Region", 
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category filter
selected_category = st.sidebar.multiselect(
    "Select Category", 
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# State filter (optional)
selected_state = st.sidebar.multiselect(
    "Select State (Optional)",
    options=df['State'].unique()
)

# Filter data based on selections
filtered_df = df.copy()

if selected_region:
    filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
if selected_category:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]
if selected_state:
    filtered_df = filtered_df[filtered_df['State'].isin(selected_state)]

# Date filtering
if 'Order Date' in df.columns and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['Order Date'] >= pd.to_datetime(start_date)) & 
        (filtered_df['Order Date'] <= pd.to_datetime(end_date))
    ]

# KPI cards
st.header("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    total_orders = filtered_df['Order ID'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"${avg_order_value:,.2f}")

with col4:
    total_customers = filtered_df['Customer ID'].nunique()
    st.metric("Unique Customers", f"{total_customers:,}")

# Charts - Row 1
st.header("📊 Sales Analysis")
col1, col2 = st.columns(2)

with col1:
    # Sales by Category
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    fig = px.pie(
        category_sales, 
        names='Category', 
        values='Sales', 
        title='Sales Distribution by Category',
        color='Category'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Sales by Region
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig = px.bar(
        region_sales, 
        x='Region', 
        y='Sales', 
        title='Total Sales by Region',
        color='Region'
    )
    st.plotly_chart(fig, use_container_width=True)

# Charts - Row 2
col1, col2 = st.columns(2)

with col1:
    # Monthly Sales Trend (if date column exists)
    if 'Order Date' in filtered_df.columns:
        monthly_sales = filtered_df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum().reset_index()
        fig = px.line(
            monthly_sales, 
            x='Order Date', 
            y='Sales', 
            title='Monthly Sales Trend',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top 10 Products by Sales
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    fig = px.bar(
        top_products, 
        x='Sales', 
        y='Product Name', 
        title='Top 10 Products by Sales',
        orientation='h'
    )
    st.plotly_chart(fig, use_container_width=True)

# Charts - Row 3
st.header("👥 Customer Analysis")
col1, col2 = st.columns(2)

with col1:
    # Sales by Customer Segment
    segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    fig = px.pie(
        segment_sales, 
        names='Segment', 
        values='Sales', 
        title='Sales by Customer Segment'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top 10 Customers
    top_customers = filtered_df.groupby('Customer Name')['Sales'].sum().nlargest(10).reset_index()
    fig = px.bar(
        top_customers, 
        x='Sales', 
        y='Customer Name', 
        title='Top 10 Customers by Sales',
        orientation='h'
    )
    st.plotly_chart(fig, use_container_width=True)

# Data table (optional)
if st.checkbox("Show Filtered Data"):
    st.header("📋 Filtered Data Preview")
    st.dataframe(filtered_df.head(100))

# Download button for filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("**Dashboard created with Streamlit** | Data: Superstore Sales Dataset")


