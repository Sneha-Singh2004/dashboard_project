# --------------------------------------------
# IMPORT LIBRARIES
# --------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# --------------------------------------------
# LOAD DATASET (LOCAL FILE)
# --------------------------------------------
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv")


# Convert Date column
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# --------------------------------------------
# 1️⃣ Year-to-Year Sales Fluctuation
# --------------------------------------------
yearly_sales = df.groupby('Year')['Automobile_Sales'].mean().reset_index()

plt.figure(figsize=(10,5))
sns.lineplot(data=yearly_sales, x='Year', y='Automobile_Sales')
plt.title("Yearly Average Automobile Sales")
plt.show()


# --------------------------------------------
# 2️⃣ Sales Trend per Vehicle Type (Recession vs Non-Recession)
# --------------------------------------------
plt.figure(figsize=(12,6))
sns.lineplot(data=df,
             x='Year',
             y='Automobile_Sales',
             hue='Vehicle_Type',
             style='Recession')
plt.title("Sales Trend per Vehicle Type (Recession vs Non-Recession)")
plt.show()


# --------------------------------------------
# 3️⃣ GDP Variation During Recession vs Non-Recession
# --------------------------------------------
gdp_data = df.groupby(['Year', 'Recession'])['GDP'].mean().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=gdp_data,
             x='Year',
             y='GDP',
             hue='Recession')
plt.title("GDP Variation During Recession vs Non-Recession")
plt.show()


# --------------------------------------------
# 4️⃣ Scatter Plot: Vehicle Price vs Sales During Recession
# --------------------------------------------
recession_data = df[df['Recession'] == 1]

plt.figure(figsize=(8,5))
sns.scatterplot(data=recession_data,
                x='Price',
                y='Automobile_Sales')
plt.title("Vehicle Price vs Sales During Recession")
plt.show()


# --------------------------------------------
# 5️⃣ Pie Chart: Advertising Expenditure (Recession vs Non-Recession)
# --------------------------------------------
ad_data = df.groupby('Recession')['Advertising_Expenditure'].sum().reset_index()

plt.figure(figsize=(6,6))
plt.pie(ad_data['Advertising_Expenditure'],
        labels=['Non-Recession', 'Recession'],
        autopct='%1.1f%%')
plt.title("Advertising Expenditure Share (Recession vs Non-Recession)")
plt.show()


# --------------------------------------------
# 6️⃣ Line Plot: Effect of Unemployment During Recession
# --------------------------------------------
unemp_data = recession_data.groupby(
    ['unemployment_rate', 'Vehicle_Type']
)['Automobile_Sales'].mean().reset_index()

plt.figure(figsize=(12,6))
sns.lineplot(data=unemp_data,
             x='unemployment_rate',
             y='Automobile_Sales',
             hue='Vehicle_Type')
plt.title("Effect of Unemployment Rate on Vehicle Type Sales During Recession")
plt.show()
