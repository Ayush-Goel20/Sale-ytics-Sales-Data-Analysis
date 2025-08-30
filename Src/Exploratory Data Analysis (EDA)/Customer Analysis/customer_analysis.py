# Customer segmentation analysis
customer_segment = df_clean.groupby('Segment').agg({
    'Customer ID': 'nunique',
    'Sales': 'sum',
    'Order ID': 'nunique'
}).rename(columns={'Customer ID': 'Unique Customers', 'Order ID': 'Total Orders'})

customer_segment['Avg Orders per Customer'] = customer_segment['Total Orders'] / customer_segment['Unique Customers']
customer_segment['Avg Sales per Customer'] = customer_segment['Sales'] / customer_segment['Unique Customers']

print("Customer Segment Analysis:")
display(customer_segment)

# Top customers by sales
top_customers = df_clean.groupby(['Customer ID', 'Customer Name'])['Sales'].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Customers by Sales:")
display(top_customers)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Customer segment by sales
axes[0].bar(customer_segment.index, customer_segment['Sales'])
axes[0].set_title('Sales by Customer Segment')
axes[0].set_ylabel('Sales ($)')

# Top customers
axes[1].barh(range(len(top_customers)), top_customers.values)
axes[1].set_yticks(range(len(top_customers)))
axes[1].set_yticklabels([f"{name}" for id, name in top_customers.index])
axes[1].set_title('Top 10 Customers by Sales')
axes[1].set_xlabel('Sales ($)')

plt.tight_layout()
plt.show()