# Calculate overall metrics
total_sales = df_clean['Sales'].sum()
total_orders = df_clean['Order ID'].nunique()
avg_order_value = total_sales / total_orders
total_customers = df_clean['Customer ID'].nunique()

# Create a summary dataframe
summary_data = {
    'Metric': ['Total Sales', 'Total Orders', 'Average Order Value', 'Total Customers'],
    'Value': [total_sales, total_orders, avg_order_value, total_customers],
    'Formatted Value': [
        f'${total_sales:,.2f}', 
        f'{total_orders:,}',
        f'${avg_order_value:.2f}',
        f'{total_customers:,}'
    ]
}

summary_df = pd.DataFrame(summary_data)
display(summary_df)

# Visualize key metrics
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Sales Performance Overview', fontsize=16)

# Sales by year
sales_by_year = df_clean.groupby('Order Year')['Sales'].sum()
axes[0, 0].bar(sales_by_year.index.astype(str), sales_by_year.values)
axes[0, 0].set_title('Total Sales by Year')
axes[0, 0].set_ylabel('Sales ($)')

# Orders by year
orders_by_year = df_clean.groupby('Order Year')['Order ID'].nunique()
axes[0, 1].bar(orders_by_year.index.astype(str), orders_by_year.values)
axes[0, 1].set_title('Total Orders by Year')
axes[0, 1].set_ylabel('Number of Orders')

# Orders by month
orders_by_month = df_clean.groupby('Order Month Name')['Order ID'].nunique()
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
orders_by_month = orders_by_month.reindex(month_order)
axes[1, 0].plot(orders_by_month.index, orders_by_month.values, marker='o')
axes[1, 0].set_title('Number of Orders by Month')
axes[1, 0].set_ylabel('Number of Orders')
plt.xticks(rotation=45)

# Shipping time distribution
axes[1, 1].hist(df_clean['Shipping Time'].dropna(), bins=20, edgecolor='black')
axes[1, 1].set_title('Shipping Time Distribution')
axes[1, 1].set_xlabel('Shipping Time (Days)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
