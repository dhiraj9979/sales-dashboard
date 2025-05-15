import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the Excel file
def load_sales_data(file_path):
    """Load sales data from Excel file"""
    df = pd.read_excel(file_path)
    
    # Convert Order Date to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    return df

# Create Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Sales Over Time Dashboard"),
    
    # Date range selector
    html.Div([
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=None,
            max_date_allowed=None,
            initial_visible_month=None
        )
    ]),
    
    # Sales line chart
    dcc.Graph(id='sales-line-chart')
])

# Callback to update the graph based on date range
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(start_date, end_date):
    try:
        # Load the data
        print(f'Loading data from sales_data.xls')
        df = load_sales_data('sales_data.xls')
        
        # Ensure Sales column is numeric
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        
        # Filter out any rows with NaN sales
        df = df.dropna(subset=['Sales'])
        
        # Aggregate sales by month
        monthly_sales = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum().reset_index()
        
        # Filter data by date range if specified
        if start_date and end_date:
            monthly_sales = monthly_sales[
                (monthly_sales['Order Date'] >= start_date) & 
                (monthly_sales['Order Date'] <= end_date)
            ]
        
        # Create line chart of monthly sales
        fig = px.line(
            monthly_sales, 
            x='Order Date', 
            y='Sales', 
            title='Monthly Sales Trend',
            labels={'Order Date': 'Month', 'Sales': 'Total Sales Amount'}
        )
        
        # Customize the chart
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Sales',
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        print(f'Error in update_graph: {str(e)}')
        raise

# Expose the Flask server for Gunicorn
server = app.server

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
