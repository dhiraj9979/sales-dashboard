import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='M')
sales = np.random.randint(1000, 10000, size=len(dates))

sample_df = pd.DataFrame({
    'Order Date': dates,
    'Sales': sales
})

# Save to Excel
sample_df.to_excel('sales_data.xls', index=False)
print("Sample sales data generated and saved to sales_data.xls")
