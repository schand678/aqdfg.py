import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Preload the CSV file directly
@st.cache_data
def load_data():
    # Load the pre-existing CSV file
    return pd.read_csv("sample_cars.csv")  # Replace with your actual file name

# Load the dataset
df = load_data()

# Display dataset preview
st.title("🚘 Vehicle Insights and Visualizations")
st.write("### Dataset Preview")
st.dataframe(df.head())

# Visualization 1: Distribution of Prices
st.subheader("Price Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
df['price'].hist(bins=15, color='skyblue', edgecolor='black', ax=ax)
ax.set_title('Distribution of Car Prices')
ax.set_xlabel('Price ($)')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# Visualization 2: Average Price by Make
st.subheader("Average Price by Car Make")
avg_price_by_make = df.groupby('make')['price'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
avg_price_by_make.plot(kind='bar', color='purple', ax=ax)
ax.set_title('Average Price by Car Make')
ax.set_xlabel('Car Make')
ax.set_ylabel('Average Price ($)')
st.pyplot(fig)

# Visualization 3: Cars Grouped by Stock Type
st.subheader("Car Stock Type Distribution")
stock_type_counts = df['stock_type'].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
stock_type_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'pink'], ax=ax)
ax.set_title('Stock Type Distribution (New vs. Used)')
ax.set_ylabel('')
st.pyplot(fig)

# Visualization 4: Correlation Heatmap
st.subheader("Feature Correlation Heatmap")
correlation_matrix = df[['price', 'mileage', 'Age']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Between Features')
st.pyplot(fig)

# Visualization 5: Number of Cars per Cluster
st.subheader("Number of Cars per Cluster")
cluster_counts = df['Cluster'].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
cluster_counts.plot(kind='bar', color='lightgreen', ax=ax)
ax.set_title('Number of Cars per Cluster')
ax.set_xlabel('Cluster ID')
ax.set_ylabel('Number of Cars')
st.pyplot(fig)
