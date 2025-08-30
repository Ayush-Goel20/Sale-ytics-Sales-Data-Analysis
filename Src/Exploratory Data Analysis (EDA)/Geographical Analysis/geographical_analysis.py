# Sales by region
sales_by_region = df_clean.groupby('Region')['Sales'].sum().sort_values(ascending=False)

# Sales by state (top 10)
sales_by_state = df_clean.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)

print("Sales by Region:")
display(sales_by_region)

print("\nTop 10 States by Sales:")
display(sales_by_state)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Sales by region
axes[0].bar(sales_by_region.index, sales_by_region.values)
axes[0].set_title('Sales by Region')
axes[0].set_ylabel('Sales ($)')

# Top states by sales
axes[1].barh(range(len(sales_by_state)), sales_by_state.values)
axes[1].set_yticks(range(len(sales_by_state)))
axes[1].set_yticklabels(sales_by_state.index)
axes[1].set_title('Top 10 States by Sales')
axes[1].set_xlabel('Sales ($)')

plt.tight_layout()
plt.show()

# Interactive map visualization
state_sales = df_clean.groupby('State')['Sales'].sum().reset_index()
fig = px.choropleth(
    state_sales,
    locations='State',
    locationmode='USA-states',
    color='Sales',
    scope='usa',
    title='Sales by State (US)',
    color_continuous_scale='Viridis'
)
fig.show()