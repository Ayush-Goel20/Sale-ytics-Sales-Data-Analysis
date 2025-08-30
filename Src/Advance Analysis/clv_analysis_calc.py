# Customer Lifetime Value Calculation
print("\n💰 Customer Lifetime Value (CLV) Analysis")
print("=" * 60)

# Calculate CLV metrics
clv_analysis = df_clean.groupby('Customer ID').agg({
    'Sales': 'sum',
    'Order ID': 'nunique',
    'Order Date': ['min', 'max'],
    'Customer Name': 'first'
}).reset_index()

# Flatten column names
clv_analysis.columns = ['Customer ID', 'Total_Revenue', 'Total_Orders', 'First_Purchase', 'Last_Purchase', 'Customer_Name']

# Calculate additional metrics
clv_analysis['Avg_Order_Value'] = clv_analysis['Total_Revenue'] / clv_analysis['Total_Orders']
clv_analysis['Customer_Lifetime_Days'] = (clv_analysis['Last_Purchase'] - clv_analysis['First_Purchase']).dt.days

# Avoid division by zero for new customers
clv_analysis['Customer_Lifetime_Days'] = clv_analysis['Customer_Lifetime_Days'].apply(lambda x: max(x, 1))

# Calculate CLV (simplified version)
clv_analysis['CLV'] = clv_analysis['Total_Revenue'] * (365 / clv_analysis['Customer_Lifetime_Days'])

# Segment customers by CLV
clv_analysis['CLV_Segment'] = pd.qcut(clv_analysis['CLV'], q=4, labels=['Low', 'Medium', 'High', 'VIP'])

# Display results
print(f"📊 Analyzed {len(clv_analysis)} customers")
print("\n🏆 Top 10 Customers by CLV:")
top_10_clv = clv_analysis.nlargest(10, 'CLV')[['Customer_Name', 'Total_Revenue', 'Total_Orders', 'Avg_Order_Value', 'CLV', 'CLV_Segment']]
display(top_10_clv.style.format({
    'Total_Revenue': '${:,.2f}',
    'Avg_Order_Value': '${:,.2f}',
    'CLV': '${:,.2f}'
}))

# CLV segmentation analysis
segment_summary = clv_analysis.groupby('CLV_Segment').agg({
    'Customer ID': 'count',
    'Total_Revenue': 'sum',
    'CLV': 'mean'
}).rename(columns={'Customer ID': 'Customer_Count', 'Total_Revenue': 'Total_Revenue'})

print("\n📈 CLV Segment Summary:")
display(segment_summary.style.format({
    'Total_Revenue': '${:,.2f}',
    'CLV': '${:,.2f}'
}))

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# CLV Distribution
axes[0].hist(clv_analysis['CLV'], bins=30, edgecolor='black', alpha=0.7)
axes[0].set_title('Customer Lifetime Value Distribution', fontsize=14)
axes[0].set_xlabel('CLV ($)', fontsize=12)
axes[0].set_ylabel('Number of Customers', fontsize=12)
axes[0].grid(True, alpha=0.3)

# Customers by CLV Segment
segment_counts = clv_analysis['CLV_Segment'].value_counts()
axes[1].bar(segment_counts.index, segment_counts.values, color=['red', 'orange', 'yellow', 'green'])
axes[1].set_title('Customers by CLV Segment', fontsize=14)
axes[1].set_xlabel('CLV Segment', fontsize=12)
axes[1].set_ylabel('Number of Customers', fontsize=12)

plt.tight_layout()
plt.show()

print(f"\n💡 Business Insight: {len(clv_analysis[clv_analysis['CLV_Segment'] == 'VIP'])} VIP customers generate maximum lifetime value!")