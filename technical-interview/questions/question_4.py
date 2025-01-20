"""
Question 4: Statistical Analysis and Error Handling

Using scipy and the cleaned dataset from Question 1, perform the following tasks:

1. Implement error handling for the following analyses:
   - Perform a one-way ANOVA test to compare prices across different categories
   - Calculate and plot the confidence intervals for mean prices in each category
   - Identify potential outliers using z-scores

2. Debug and fix the following code snippet that attempts to perform a chi-square test:
   ```python
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
   ```

3. Implement proper logging to track:
   - Any statistical assumptions violations
   - Data type mismatches
   - Invalid calculations

Your solution should be robust against various edge cases and include appropriate error messages.
"""

# Your code here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the cleaned dataset
file_path = r'.\cleaned_sales_data.csv'
sales_data = pd.read_csv(file_path)

# Ensure 'sale_date' is in datetime format
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')

# Step 1: Perform a one-way ANOVA test
try:
    categories = sales_data['category'].unique()
    price_groups = [sales_data[sales_data['category'] == category]['price'] for category in categories]
    anova_stat, anova_p = stats.f_oneway(*price_groups)
    logging.info(f"ANOVA test completed: F-statistic={anova_stat:.4f}, p-value={anova_p:.4f}")
except Exception as e:
    logging.error(f"Error performing ANOVA test: {e}")

# Step 2: Calculate and plot confidence intervals for mean prices
try:
    conf_intervals = {}
    for category in categories:
        prices = sales_data[sales_data['category'] == category]['price']
        mean_price = np.mean(prices)
        sem = stats.sem(prices)
        ci = stats.t.interval(0.95, len(prices)-1, loc=mean_price, scale=sem)
        conf_intervals[category] = ci
        logging.info(f"Confidence interval for {category}: {ci}")

    # Plot confidence intervals
    plt.figure(figsize=(10, 6))
    for i, category in enumerate(categories):
        ci = conf_intervals[category]
        plt.errorbar(i, np.mean(sales_data[sales_data['category'] == category]['price']),
                     yerr=[[np.mean(sales_data[sales_data['category'] == category]['price']) - ci[0]],
                           [ci[1] - np.mean(sales_data[sales_data['category'] == category]['price'])]],
                     fmt='o', label=category, capsize=5)
    plt.xticks(range(len(categories)), categories, rotation=45)
    plt.title('Confidence Intervals for Mean Prices by Category')
    plt.xlabel('Category')
    plt.ylabel('Mean Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./confidence_intervals.png')
    plt.show()
except Exception as e:
    logging.error(f"Error calculating confidence intervals: {e}")

# Step 3: Identify potential outliers using z-scores
try:
    sales_data['z_score'] = stats.zscore(sales_data['price'])
    outliers = sales_data[np.abs(sales_data['z_score']) > 3]
    logging.info(f"Identified {len(outliers)} outliers")
except Exception as e:
    logging.error(f"Error identifying outliers: {e}")

# Debug and fix chi-square function
def perform_chi_square(data):
    try:
        observed = data.groupby(['category', 'status']).size().unstack(fill_value=0)
        chi2, p_value, _, _ = stats.chi2_contingency(observed)
        logging.info(f"Chi-square test completed: Chi2={chi2:.4f}, p-value={p_value:.4f}")
        return chi2, p_value
    except Exception as e:
        logging.error(f"Error performing chi-square test: {e}")
        return None, None

# Example call to chi-square function
if 'status' in sales_data.columns:
    chi2, p_value = perform_chi_square(sales_data)
else:
    logging.warning("Column 'status' is not present in the dataset.")