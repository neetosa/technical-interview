"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations:

1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files
"""

# Your code here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the cleaned dataset

file_path = r'.\cleaned_sales_data.csv'
sales_data = pd.read_csv(file_path)

# Ensure 'sale_date' is in datetime format

sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')

# Step 1: Line Plot - Daily Sales Trends
# I believe this is not the best type of graph to visualize this data. 
# Unless it is extremely necessary to visualize daily sales, I believe the best way would be to group them into monthly sales.

sales_data['daily_sales'] = sales_data.groupby('sale_date')['price'].transform('sum')
daily_sales = sales_data.groupby('sale_date')['price'].sum()
daily_sales_ma7 = daily_sales.rolling(window=7).mean()

# To make the graph more visually pleasing, add the 'alpha' parameter and reduce the line size to 0.8. 
# I left the colors in yellow and dark violet because the Agromai logo is in a color similar to violet.

# Calculate the trend line
z = np.polyfit(range(len(daily_sales)), daily_sales.values, 1) # Calculate the linear trend
p = np.poly1d(z)

plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, p(range(len(daily_sales))), ls = '-', label="Trend Line", color='gold', lw = 1.5)
plt.plot(daily_sales_ma7.index, daily_sales_ma7, label='7-Day Moving Average', color='darkviolet', ls='-')
plt.title('Daily Sales Trends with 7-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.yticks(np.arange(0,201, 50))
plt.grid(True)
plt.tight_layout()
plt.savefig('./daily_sales_trends.png')


# Step 2: Bar Plot - Total Sales by Category with Error Bars

category_sales = sales_data.groupby('category').agg(total_sales=('price', 'sum'), std_dev=('price', 'std'))

# Select categories

categories = category_sales.index
x_pos = np.arange(len(categories))

plt.figure(figsize=(10, 6))
plt.bar(x_pos, category_sales['total_sales'], yerr=category_sales['std_dev'], color='blueviolet', capsize=5)
plt.title('Total Sales by Category with Error Bars')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.yticks(np.arange(0, 20001, 5000))
plt.xticks(x_pos, categories, rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(r'.\sales_by_category.png')

# Step 3: Scatter Plot - Quantity vs. Price Colored by Category
# Group by category and quantity, then sum the prices

grouped_data = sales_data.groupby(['category', 'quantity'])['price'].sum().reset_index()

# Plot aggregated data

plt.figure(figsize=(12, 6))

categories = grouped_data['category'].unique()
colors = plt.cm.Set1(np.linspace(0, 1, len(categories)))

for i, category in enumerate(categories):
   category_data = grouped_data[grouped_data['category'] == category]
   plt.scatter(category_data['quantity'], category_data['price'], 
      label=category, color=colors[i], marker='o')
    
   if len(category_data) > 0:  # Ensure there is enough data for regression
      slope, intercept, _, _, _ = linregress(category_data['quantity'], category_data['price'])
        
      # Create values ​​for the trend line
      x_values = np.linspace(category_data['quantity'].min(), category_data['quantity'].max(), 100)
      y_values = slope * x_values + intercept
        
      # Ploting tredline
      plt.plot(x_values, y_values, color=colors[i], linestyle='-', lw = 1.3, label=f'{category} Trend')

# Plot settings
plt.title('Aggregated Price by Quantity for Each Category')
plt.xlabel('Quantity')
plt.ylabel('Total Price')
plt.yticks(np.arange(1000,3001, 500))
plt.legend(title='Category', loc = (1.05,0))
plt.grid(True)
plt.tight_layout()
plt.savefig(r'.\quantity_per_price.png')
plt.show()