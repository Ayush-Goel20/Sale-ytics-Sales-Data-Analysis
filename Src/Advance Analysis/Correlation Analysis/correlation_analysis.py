# Correlation analysis - using available columns
# From your dataset preview, we have 'Sales' but not 'Quantity' or 'Shipping Time'
# Let's use what's available or create relevant columns

# Check what numeric columns we have
numeric_columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
print("Available numeric columns:", numeric_columns)

# Create some derived metrics for correlation analysis
df_clean['Order Month'] = df_clean['Order Date'].dt.month
df_clean['Order Year'] = df_clean['Order Date'].dt.year

# If we need to create a quantity-like metric, we might need to use other approaches
# Since we don't have quantity, let's use available metrics

# Use available numeric columns for correlation
available_numeric_cols = ['Sales', 'Postal Code', 'Order Month', 'Order Year']
correlation_matrix = df_clean[available_numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Matrix of Available Numeric Features')
plt.tight_layout()
plt.show()

# Create a Date column for time series analysis (first day of each month)
df_clean['Date'] = df_clean['Order Date'].dt.to_period('M').dt.to_timestamp()

# Sales distribution by product category over time
category_time_series = df_clean.groupby(['Date', 'Category'])['Sales'].sum().reset_index()

plt.figure(figsize=(14, 8))
colors = ['blue', 'orange', 'green']  # Different colors for each category
for i, category in enumerate(category_time_series['Category'].unique()):
    category_data = category_time_series[category_time_series['Category'] == category]
    plt.plot(category_data['Date'], category_data['Sales'], label=category, 
             linewidth=2, marker='o', color=colors[i])

plt.title('Sales Trend by Category Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Additional analysis: Top 10 products by sales
top_products = df_clean.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
top_products.plot(kind='barh', color='skyblue')
plt.title('Top 10 Products by Sales', fontsize=16)
plt.xlabel('Total Sales ($)', fontsize=12)
plt.ylabel('Product Name', fontsize=12)
plt.gca().invert_yaxis()  # Display highest at the top
plt.tight_layout()
plt.show()

# Sales by region analysis
region_sales = df_clean.groupby('Region')['Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
region_sales.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
plt.title('Total Sales by Region', fontsize=16)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Customer segment analysis
segment_analysis = df_clean.groupby('Segment').agg({
    'Sales': 'sum',
    'Order ID': 'nunique'
}).rename(columns={'Order ID': 'Number of Orders'})

segment_analysis['Average Order Value'] = segment_analysis['Sales'] / segment_analysis['Number of Orders']

print("Customer Segment Analysis:")
display(segment_analysis)

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Sales by segment
ax1.bar(segment_analysis.index, segment_analysis['Sales'], color='lightblue')
ax1.set_title('Total Sales by Customer Segment')
ax1.set_ylabel('Sales ($)')

# Average order value by segment
ax2.bar(segment_analysis.index, segment_analysis['Average Order Value'], color='lightgreen')
ax2.set_title('Average Order Value by Segment')
ax2.set_ylabel('Dollars ($)')

plt.tight_layout()
plt.show()