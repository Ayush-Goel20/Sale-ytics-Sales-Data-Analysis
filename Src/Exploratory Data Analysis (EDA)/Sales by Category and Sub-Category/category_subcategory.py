# Sales by category
sales_by_category = df_clean.groupby('Category')['Sales'].sum().sort_values(ascending=False)

# Sales by sub-category
sales_by_subcategory = df_clean.groupby(['Category', 'Sub-Category'])['Sales'].sum().sort_values(ascending=False)

print("Sales by Category:")
display(sales_by_category)

print("\nTop 10 Sub-Categories by Sales:")
display(sales_by_subcategory.head(10))

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Sales by category
axes[0].pie(sales_by_category.values, labels=sales_by_category.index, autopct='%1.1f%%')
axes[0].set_title('Sales Distribution by Category')

# Sales by sub-category (top 10)
top10_subcat_sales = sales_by_subcategory.head(10)
axes[1].barh(range(len(top10_subcat_sales)), top10_subcat_sales.values)
axes[1].set_yticks(range(len(top10_subcat_sales)))
axes[1].set_yticklabels([f"{cat[0]} - {cat[1]}" for cat in top10_subcat_sales.index])
axes[1].set_title('Top 10 Sub-Categories by Sales')
axes[1].set_xlabel('Sales ($)')

plt.tight_layout()
plt.show()

# Interactive visualization with Plotly
fig = px.sunburst(
    df_clean, 
    path=['Category', 'Sub-Category'], 
    values='Sales',
    title='Sales Distribution by Category and Sub-Category'
)
fig.show()