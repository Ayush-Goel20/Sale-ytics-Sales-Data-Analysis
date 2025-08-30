# RFM Analysis
print("\n🏆 RFM Analysis (Recency, Frequency, Monetary)")
print("=" * 60)

from datetime import datetime

# Calculate RFM metrics
current_date = df_clean['Order Date'].max() + pd.Timedelta(days=1)

rfm_df = df_clean.groupby('Customer ID').agg({
    'Order Date': lambda x: (current_date - x.max()).days,  # Recency
    'Order ID': 'nunique',                                  # Frequency  
    'Sales': 'sum',                                         # Monetary
    'Customer Name': 'first'                                # Customer name
}).rename(columns={
    'Order Date': 'Recency', 
    'Order ID': 'Frequency', 
    'Sales': 'Monetary',
    'Customer Name': 'Customer_Name'
})

# Create RFM scores (1-5, with 5 being best)
rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# Convert scores to numeric
rfm_df['R_Score'] = rfm_df['R_Score'].astype(int)
rfm_df['F_Score'] = rfm_df['F_Score'].astype(int)
rfm_df['M_Score'] = rfm_df['M_Score'].astype(int)

# Combine scores
rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
rfm_df['RFM_Sum'] = rfm_df['R_Score'] + rfm_df['F_Score'] + rfm_df['M_Score']

# Segment customers
def rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 2:
        return 'Potential Loyalists'
    elif row['R_Score'] >= 2:
        return 'New Customers'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 2:
        return 'At Risk'
    elif row['R_Score'] <= 1 and row['F_Score'] <= 2:
        return 'Cannot Lose'
    else:
        return 'Need Attention'

rfm_df['Segment'] = rfm_df.apply(rfm_segment, axis=1)

# Display results
print(f"📊 Analyzed {len(rfm_df)} customers for RFM analysis")
print("\n🎯 Customer Segmentation Results:")
segment_counts = rfm_df['Segment'].value_counts()
display(segment_counts)

print("\n🏆 Top Customers by RFM Segment:")
# Show top customers from each segment
for segment in rfm_df['Segment'].unique():
    segment_customers = rfm_df[rfm_df['Segment'] == segment].nlargest(3, 'RFM_Sum')
    print(f"\n{segment}:")
    for _, row in segment_customers.iterrows():
        print(f"  - {row['Customer_Name']}: R{row['R_Score']}F{row['F_Score']}M{row['M_Score']} (${row['Monetary']:,.2f})")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# RFM Segmentation Pie Chart
segment_counts.plot(kind='pie', autopct='%1.1f%%', ax=axes[0, 0])
axes[0, 0].set_title('Customer RFM Segmentation', fontsize=14)
axes[0, 0].set_ylabel('')

# Recency Distribution
axes[0, 1].hist(rfm_df['Recency'], bins=20, edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Recency Distribution (Days since last purchase)', fontsize=14)
axes[0, 1].set_xlabel('Days')
axes[0, 1].set_ylabel('Number of Customers')

# Frequency Distribution
axes[1, 0].hist(rfm_df['Frequency'], bins=20, edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Frequency Distribution (Number of orders)', fontsize=14)
axes[1, 0].set_xlabel('Orders')
axes[1, 0].set_ylabel('Number of Customers')

# Monetary Distribution
axes[1, 1].hist(rfm_df['Monetary'], bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Monetary Distribution (Total spending)', fontsize=14)
axes[1, 1].set_xlabel('Total Spending ($)')
axes[1, 1].set_ylabel('Number of Customers')

plt.tight_layout()
plt.show()

print(f"\n💡 Business Insight: You have {segment_counts.get('Champions', 0)} Champion customers who are recent, frequent, and high-spending!")