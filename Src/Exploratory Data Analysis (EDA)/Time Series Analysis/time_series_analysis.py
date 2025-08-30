# Create a time series of monthly sales
monthly_sales = df_clean.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly_sales['Date'] = pd.to_datetime(monthly_sales['Order Year'].astype(str) + '-' + monthly_sales['Order Month'].astype(str) + '-01')
monthly_sales = monthly_sales.sort_values('Date')

# Create a time series of monthly orders
monthly_orders = df_clean.groupby(['Order Year', 'Order Month'])['Order ID'].nunique().reset_index()
monthly_orders['Date'] = pd.to_datetime(monthly_orders['Order Year'].astype(str) + '-' + monthly_orders['Order Month'].astype(str) + '-01')
monthly_orders = monthly_orders.sort_values('Date')

print("Monthly Sales Trend:")
display(monthly_sales.head(10))

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Monthly sales trend
axes[0].plot(monthly_sales['Date'], monthly_sales['Sales'], marker='o', linewidth=2)
axes[0].set_title('Monthly Sales Trend', fontsize=14)
axes[0].set_ylabel('Sales ($)', fontsize=12)
axes[0].grid(True, alpha=0.3)

# Monthly orders trend
axes[1].plot(monthly_orders['Date'], monthly_orders['Order ID'], marker='o', color='orange', linewidth=2)
axes[1].set_title('Monthly Orders Trend', fontsize=14)
axes[1].set_ylabel('Number of Orders', fontsize=12)
axes[1].set_xlabel('Date', fontsize=12)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Interactive visualization with Plotly
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add sales trace
fig.add_trace(
    go.Scatter(
        x=monthly_sales['Date'],
        y=monthly_sales['Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='blue', width=2)
    ),
    secondary_y=False,
)

# Add orders trace
fig.add_trace(
    go.Scatter(
        x=monthly_orders['Date'],
        y=monthly_orders['Order ID'],
        mode='lines+markers',
        name='Orders',
        line=dict(color='orange', width=2)
    ),
    secondary_y=True,
)

# Update layout
fig.update_layout(
    title='Monthly Sales and Orders Trends',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Sales ($)', side='left', showgrid=False),
    yaxis2=dict(title='Number of Orders', side='right', overlaying='y', showgrid=False),
    legend=dict(x=0, y=1),
    hovermode='x unified'
)

fig.show()