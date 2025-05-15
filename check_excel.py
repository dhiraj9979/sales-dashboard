import pandas as pd

# Read the Excel file
try:
    df = pd.read_excel('sales_data.xls')
    
    # Print basic information
    print("Excel File Analysis:")
    print("-" * 30)
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Check column types
    print("\nColumn Types:")
    print(df.dtypes)
    
    # Check first few rows
    print("\nFirst 5 Rows:")
    print(df.head())
    
    # Check for any issues with date and sales columns
    print("\nDate Column Check:")
    try:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        print("Order Date column converted successfully")
        print(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")
    except Exception as e:
        print(f"Error converting Order Date: {e}")
    
    print("\nSales Column Check:")
    try:
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        print("Sales column converted to numeric")
        print(f"Sales Range: {df['Sales'].min()} to {df['Sales'].max()}")
        print(f"Number of NaN values: {df['Sales'].isna().sum()}")
    except Exception as e:
        print(f"Error converting Sales: {e}")

except Exception as e:
    print(f"Error reading Excel file: {e}")
