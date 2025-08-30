# Create a more detailed monthly analysis
monthly_analysis = df_clean.groupby(['Order Year', 'Order Month Name']).agg({
    'Sales': 'sum',
    'Order ID': 'nunique'
}).reset_index()

# Reorder months correctly
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_analysis['Order Month Name'] = pd.Categorical(monthly_analysis['Order Month Name'], 
                                                     categories=month_order, ordered=True)
monthly_analysis = monthly_analysis.sort_values(['Order Year', 'Order Month Name'])

# Pivot for better visualization
pivot_sales = monthly_analysis.pivot(index='Order Month Name', columns='Order Year', values='Sales')

plt.figure(figsize=(14, 8))
pivot_sales.plot(kind='line', marker='o', linewidth=2)
plt.title('Monthly Sales Trends by Year', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.legend(title='Year')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Monthly Sales Summary:")
display(monthly_analysis.groupby('Order Month Name')['Sales'].mean().sort_values(ascending=False))