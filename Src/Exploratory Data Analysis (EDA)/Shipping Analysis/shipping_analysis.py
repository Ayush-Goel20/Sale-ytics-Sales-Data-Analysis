# Shipping mode analysis
shipping_analysis = df_clean.groupby('Ship Mode').agg({
    'Order ID': 'nunique',
    'Sales': 'sum',
    'Shipping Time': 'mean'
}).rename(columns={'Order ID': 'Total Orders', 'Shipping Time': 'Avg Shipping Time'})

shipping_analysis['Avg Order Value'] = shipping_analysis['Sales'] / shipping_analysis['Total Orders']

print("Shipping Mode Analysis:")
display(shipping_analysis)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Orders by ship mode
axes[0, 0].bar(shipping_analysis.index, shipping_analysis['Total Orders'])
axes[0, 0].set_title('Orders by Shipping Mode')
axes[0, 0].set_ylabel('Number of Orders')

# Sales by ship mode
axes[0, 1].bar(shipping_analysis.index, shipping_analysis['Sales'])
axes[0, 1].set_title('Sales by Shipping Mode')
axes[0, 1].set_ylabel('Sales ($)')

# Avg shipping time by mode
axes[1, 0].bar(shipping_analysis.index, shipping_analysis['Avg Shipping Time'])
axes[1, 0].set_title('Average Shipping Time by Mode')
axes[1, 0].set_ylabel('Days')

# Avg order value by mode
axes[1, 1].bar(shipping_analysis.index, shipping_analysis['Avg Order Value'])
axes[1, 1].set_title('Average Order Value by Shipping Mode')
axes[1, 1].set_ylabel('Dollars ($)')

plt.tight_layout()
plt.show()