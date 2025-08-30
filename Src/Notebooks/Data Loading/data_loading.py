# Load the Superstore dataset
# Note: If you don't have the dataset, we'll generate dummy data
try:
    # Try to load from a local file or URL
    df = pd.read_csv('Data.csv')
    print("Superstore dataset loaded successfully!")
except:
    # Generate dummy data if the file is not available
    print("Superstore dataset not found. Generating dummy data...")
    np.random.seed(42)
    
    # Create dates
    dates = pd.date_range(start='2018-01-01', end='2021-12-31', freq='D')
    
    # Create product categories and sub-categories
    categories = ['Furniture', 'Office Supplies', 'Technology']
    sub_categories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Pens', 'Paper', 'Binders', 'Storage'],
        'Technology': ['Phones', 'Computers', 'Accessories']
    }
    
    # Create regions and states
    regions = ['West', 'East', 'South', 'Central']
    states = {
        'West': ['California', 'Washington', 'Oregon'],
        'East': ['New York', 'Pennsylvania', 'Massachusetts'],
        'South': ['Texas', 'Florida', 'Georgia'],
        'Central': ['Illinois', 'Ohio', 'Michigan']
    }
    
    # Generate sample data
    n_samples = 5000
    data = {
        'Order Date': np.random.choice(dates, n_samples),
        'Category': np.random.choice(categories, n_samples),
        'Sub-Category': [],
        'Sales': np.random.lognormal(mean=5, sigma=1.5, size=n_samples),
        'Quantity': np.random.randint(1, 10, n_samples),
        'Discount': np.random.uniform(0, 0.5, n_samples),
        'Profit': [],
        'Region': np.random.choice(regions, n_samples),
        'State': [],
        'Product ID': [f'PROD-{i:05d}' for i in range(n_samples)]
    }
    
    # Generate sub-categories, states, and profits based on other fields
    for i in range(n_samples):
        cat = data['Category'][i]
        data['Sub-Category'].append(np.random.choice(sub_categories[cat]))
        
        region = data['Region'][i]
        data['State'].append(np.random.choice(states[region]))
        
        # Profit depends on sales, discount, and some randomness
        base_profit = data['Sales'][i] * np.random.uniform(0.1, 0.3)
        discount_impact = data['Sales'][i] * data['Discount'][i] * np.random.uniform(0.5, 1.5)
        data['Profit'].append(base_profit - discount_impact + np.random.normal(0, 10))
    
    df = pd.DataFrame(data)
    print("Dummy data generated successfully!")

# Display basic information about the dataset
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
display(df.head())

print("\nDataset info:")
df.info()