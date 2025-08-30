# Create a copy of the original dataframe
from google.colab import files
df_clean = df.copy()

# Convert date columns to datetime
df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'], format='%d-%m-%Y')
df_clean['Ship Date'] = pd.to_datetime(df_clean['Ship Date'], format='%d-%m-%Y')

# Extract temporal features
df_clean['Order Year'] = df_clean['Order Date'].dt.year
df_clean['Order Month'] = df_clean['Order Date'].dt.month
df_clean['Order Month Name'] = df_clean['Order Date'].dt.month_name()
df_clean['Order Day of Week'] = df_clean['Order Date'].dt.day_name()
df_clean['Order Quarter'] = df_clean['Order Date'].dt.quarter

# Calculate shipping time in days
df_clean['Shipping Time'] = (df_clean['Ship Date'] - df_clean['Order Date']).dt.days

# Handle missing values in Postal Code
df_clean['Postal Code'] = df_clean['Postal Code'].fillna(0).astype(int)

# Check for any other missing values
print("Missing values after cleaning:")
print(df_clean.isnull().sum())

# Display cleaned data info
print("\nCleaned dataset info:")
df_clean.info()

# Save in Colab VM
df_clean.to_csv("cleaned_sales_data.csv", index=False)
# Download to your computer
files.download("cleaned_sales_data.csv")