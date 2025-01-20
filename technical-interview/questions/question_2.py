"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

# Your code here

import pandas as pd
import urllib.request

# Step 1: Load and examine the dataset

# Raw file URL on GitHub
url = r"https://raw.githubusercontent.com/neetosa/technical-interview/main//technical-interview/data/customer_purchases.csv"

# File name to save locally
output_file = "customer_purchases.csv"

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

file_path = r'.\customer_purchases.csv'
customer_data = pd.read_csv(file_path)

# Display the first few rows of the dataset just to visualize some exemple

print('*'*100)
print("\nInitial Dataset Preview:")
print(customer_data.head())
print('*'*100)

# Print out general info of the dataset for examination

print("\nDataset Information:")
print(customer_data.info())
print('*'*100)

# Print out some statistical descriptions of the dataset. 
# Helps to have a general understanding of the data and facilitates some future insites

print("\nStatistical description of columns:")
print(customer_data.describe(include = 'all'))
print('*'*100)

# Ensure 'purchase_date' is in datetime format

customer_data['purchase_date'] = pd.to_datetime(customer_data['purchase_date'], errors='coerce')
print("\nConverted 'purchase_date' to datetime format.\n")
print('*'*100)

# Step 2: Calculate metrics per customer

# I created the 'customer_metrics' variable to help with the 'reset_index()' method to maintain old indices.
# So when I use the 'nlargest' and 'nsmallest' methods, the consumer indexes are kept correct

customer_metrics = customer_data.groupby('customer_id').agg(
    total_spent=('amount', 'sum'),
    average_purchase_value=('amount', 'mean'),
    number_of_purchases=('amount', 'count'),
    most_frequent_category=('category', lambda x: x.mode()[0])
).reset_index()

# Rounding the values ​​to two decimal places

customer_metrics['average_purchase_value'] = customer_metrics['average_purchase_value'].round(2)

# Printing out the customers metrics

print("\nCustomer Metrics:\n")
print(customer_metrics.head())
print('*'*100)

# Step 3: Create summary DataFrame for top and bottom customers

# Top 5 customers by total spend

top_customers = customer_metrics.nlargest(5, 'total_spent')

# Bottom 5 customers by total spend

bottom_customers = customer_metrics.nsmallest(5, 'total_spent')

print("\nTop 5 Customers by Total Spend:\n")
print(top_customers)
print('*'*100)

print("\nBottom 5 Customers by Total Spend:\n")
print(bottom_customers)
print('*'*100)

# Step 4: Calculate monthly purchase trends

# I used the 'to_period' method to create the 'month' column with specific periods in months. 
# This will make it easier to use 'groupby' later

customer_data['month'] = customer_data['purchase_date'].dt.to_period('M')

# Total sales per month

monthly_sales = customer_data.groupby('month')['amount'].sum()

# Average purchase value per month

monthly_avg_purchase = customer_data.groupby('month')['amount'].mean()

print("\nTotal Sales Per Month:\n")
print(monthly_sales)
print('*'*100)

print("\nAverage Purchase Value Per Month:\n")
print(monthly_avg_purchase)
print('*'*100)

# Bonus: Identify customers who haven't made a purchase in the last 3 months
# I will assume that the most recent date is the last purchase date in the dataset
# I will use the ~ operator on the inactive_customers line as a logical negation operator.
# Therefore, I make a list of active consumers and then select the inactive ones

recent_date = customer_data['purchase_date'].max()
three_months_ago = recent_date - pd.DateOffset(months=3)
inactive_customers = customer_metrics[~customer_metrics['customer_id'].isin(
    customer_data[customer_data['purchase_date'] > three_months_ago]['customer_id']
)]

# The code below creates a new column 'last_date_purche' for the 'inactive_costumers' dataset. 
# I believe this is an important data for future uses.

last_purchase_dates = customer_data.groupby('customer_id')['purchase_date'].max().reset_index()
inactive_customers = inactive_customers.merge(last_purchase_dates, on='customer_id', how='left')
inactive_customers.rename(columns={'purchase_date': 'last_purchase_date'}, inplace=True)

# Print out de 'customer_id' of the inactive costumers for the last 3 months

print("\nCustomers who haven't made a purchase in the last 3 months:\n")
print(inactive_customers['customer_id'])

# Creating the monthly data report, although it is not directly requested, I believe it is useful to save the monthly data in a spreadsheet for future use

monthly_report = pd.DataFrame({
    'Month': monthly_sales.index,
    'Sales': monthly_sales.values,
    'Average purchases': monthly_avg_purchase.values
})

# Save results
customer_metrics.to_csv(r'.\customer_metrics.csv', index=False)
top_customers.to_csv(r'.\top_customers.csv', index=False)
bottom_customers.to_csv(r'.\bottom_customers.csv', index=False)
inactive_customers.to_csv(r'.\inactive_customers.csv', index=False)
monthly_report.to_csv(r'.\monthly_report.csv', index=False)
print("\nAnalysis results saved to files.")