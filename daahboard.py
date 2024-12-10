
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("### Preview of Uploaded Data")
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
else:
    st.warning("Please upload a CSV file to see visualizations.")
