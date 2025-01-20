"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

# Your code here

import pandas as pd
import numpy as np
import urllib.request

# Raw file URL on GitHub
url = r"https://raw.githubusercontent.com/neetosa/technical-interview/main//technical-interview/data/sales_data.csv"

# File name to save locally
output_file = "sales_data.csv"

try:
    # Download content
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    
    # Save content to a local file
    with open(output_file, 'w') as file:
        file.write(content)
    
    print(f"Código salvo em {output_file}")
except Exception as e:
    print(f"Erro ao baixar o arquivo: {e}")

file_path = r'.\sales_data.csv'
sales_data = pd.read_csv(file_path)

# Display the first few rows of the dataset just to visualize some exemple
# I chose to add '*' to make the output easier to read in the terminal

print('*'*100)
print("Initial Dataset Preview:")
print(sales_data.head())
print('*'*100)

# Print out general info of the dataset for examination

print("Dataset Information:")
print(sales_data.info())
print('*'*100)

# Print out some statistical descriptions of the dataset. 
# Helps to have a general understanding of the data and facilitates some future insites

print("Statistical description of columns:")
print(sales_data.describe(include='all'))
print('*'*100)

# Calculates the total number of missing values of missing values handled. 
# I managed to put the data into a dictionary to make it easier to organize and view in the future.

missing_values_handled = {
    'price': sales_data['price'].isna().sum(),
    'category': sales_data['category'].isna().sum()
}

# Step 2: Data Cleaning

# Handle missing values in the 'price' column by replacing with the mean 
# and handle missing values in the 'category' column by replacing with the mode 
# printing a confirmation message.

price_mean = sales_data['price'].mean()
sales_data['price'].fillna(price_mean)
category_mode = sales_data['category'].mode()[0]
sales_data['category'].fillna(category_mode)

# Printing a confirmation message

print(f"\n\nReplaced missing 'price' values with mean: {price_mean:.2f}")
print(f"Replaced missing 'category' values with mode: {category_mode}\n\n")
print('*'*100)

# Convert 'sale_date' to datetime format

sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')
print("\n\nConverted 'sale_date' to datetime format.")

# Step 3: Create a summary

# Total number of sales per category

sales_per_category = sales_data.groupby('category').size()

# Average price per category
# Since we are talking about money i'll round the prices using two decimal places.
# And knowing the number of sales is not that big i believe that is no need to use 3 decimals.

average_price_per_category = np.around(sales_data.groupby('category')['price'].mean(),2)

# Display the summaries

print("\nSummary of Total Sales Per Category and Average Price Per Category:\n")
print(sales_per_category)
print(average_price_per_category)
print('*'*100)

print(f"\nNumber of Missing Values Handled: {missing_values_handled}\n")

print('*'*100)

# Save the cleaned dataset for further analysis

cleaned_file_path = r'.\cleaned_sales_data.csv'

sales_data.to_csv(cleaned_file_path, index=False)

# Printing a confirmation message

print(f"\nCleaned dataset saved to {cleaned_file_path}\n")
print('*'*100)