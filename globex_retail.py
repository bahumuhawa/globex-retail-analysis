# Import libraries for PDF extraction, data analysis, and visualization
import tabula
import pandas as pd
import matplotlib.pyplot as plt

# Define input PDF and output CSV file paths
inp = "globex_data.pdf"
oup = "globex_data.csv"

# Read all PDF tables into a DataFrame(s)
df = tabula.read_pdf(input_path=inp, pages="all")

# Convert PDF tables directly into a CSV file
tabula.convert_into(input_path=inp, output_path=oup, output_format="csv", pages="all", stream=True)

# Load the converted CSV file into a DataFrame
df = pd.read_csv("globex_data.csv")

# Display the first rows and dataset info
print(df.head())
print(df.info())

# Convert Order_Date column to datetime format
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Check for missing values in the dataset
print(df.isnull().sum())

# Create a Revenue column from Quantity, Price, and Discount
df['Revenue'] = df['Quantity'] * df['Price'] * (1 - df['Discount'])

# Calculate revenue by product category
category_revenue = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
print(category_revenue)

# Calculate revenue by product category
subcategory_revenue = df.groupby('Product_Sub_Category')['Revenue'].sum().sort_values(ascending=False)
print(subcategory_revenue)

# Summarize total revenue and orders per customer
customer_orders = df.groupby('Customer_ID').agg({'Revenue': 'sum', 'Order_ID': 'nunique'})

# Calculate Average Order Value (AOV) for each customer
customer_orders['AOV'] = customer_orders['Revenue'] / customer_orders['Order_ID']
print(customer_orders.sort_values(by='AOV', ascending=False).head())

# Set revenue threshold for top 10% customers
threshold = customer_orders['Revenue'].quantile(0.90)

# Filter data for high-value customers
high_value_customers = df[df['Customer_ID'].isin(customer_orders[customer_orders['Revenue'] > threshold].index)]

# Calculate the average discount for high-value customers
avg_discount = high_value_customers['Discount'].mean()
print(avg_discount)

# Find top customer locations among high-value customers
top_locations = high_value_customers.groupby('Customer_Location')['Customer_ID'].nunique().sort_values(ascending=False)
print(top_locations)

# Calculate average discount and revenue per category
discount_impact = df.groupby('Product_Category').agg({'Discount': 'mean', 'Revenue': 'sum'})
print(discount_impact)

# Extract month from Order_Date for trend analysis
df['Month'] = df['Order_Date'].dt.to_period('M')

# Calculate monthly total revenue
monthly_revenue = df.groupby('Month')['Revenue'].sum()
print(monthly_revenue)

# Plot revenue by product category as a bar chart
category_revenue.plot(kind='bar', title='Revenue by Product Category')
plt.ylabel('Revenue')
plt.show()
