import streamlit as st

# Set page configuration
st.set_page_config(page_title="Vehicle Make Clustering",)

# Main Title
st.title("Vehicle Make Clustering: Unlocking Sales Insights")

# Introduction Section
st.subheader("About the Project")
st.write("""
 This initiative leverages data science techniques to analyze 
and group vehicle makes based on their unique attributes and sales performance. The dataset utilized contains 
comprehensive information, including:
- **Vehicle Specifications**: Make, model, year, mileage, and price.
- **Sales Data**: Transaction details from multiple dealerships over a specific timeframe.
""")

# Problem Statement
st.subheader("Understanding the Challenge")
st.write("""
Dealerships often face challenges such as:
- Identifying top-performing vehicle makes.
- Managing inventory efficiently.
- Developing data-backed marketing strategies.

This project aims to address these issues by uncovering patterns in vehicle sales and clustering vehicle makes 
for actionable insights.
""")

# Objectives Section
st.subheader("What We Aim to Achieve")
st.write("""
Our project focuses on the following objectives:
1. Conducting an **Exploratory Data Analysis (EDA)** to identify sales patterns.
2. Building a **Clustering Model** to categorize vehicle makes based on their features.
3. Utilizing the clusters to:
   - Recognize high-demand vehicle categories.
   - Optimize dealership inventory planning.
   - Enhance marketing strategies for better customer engagement.
""")


# Call to Action
st.subheader("Join Us on This Journey")
st.write("""
This project is a step towards innovation in the automotive industry. Let’s harness the power of data to drive 
better business outcomes and revolutionize how dealerships operate!
""")
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file):
    """Load the dataset and cache it for performance."""
    return pd.read_csv(file)

@st.cache_data
def recommend_by_cluster_price_and_mileage(input_make, input_price, input_mileage, df2, cluster_column='Cluster', price_tolerance=2000, mileage_tolerance=5000, top_n=5):
    """Recommend vehicles efficiently with caching, including mileage-based filtering."""
    # Identify the cluster of the input vehicle make
    input_cluster = df2[df2['make'] == input_make][cluster_column].iloc[0]

    # Filter vehicles by the same cluster
    cluster_data = df2[df2[cluster_column] == input_cluster]

    # Filter vehicles within the price and mileage range
    price_lower_bound = input_price - price_tolerance
    price_upper_bound = input_price + price_tolerance
    mileage_lower_bound = input_mileage - mileage_tolerance
    mileage_upper_bound = input_mileage + mileage_tolerance

    recommendations = cluster_data[
        (cluster_data['price'] >= price_lower_bound) & 
        (cluster_data['price'] <= price_upper_bound) &
        (cluster_data['mileage'] >= mileage_lower_bound) & 
        (cluster_data['mileage'] <= mileage_upper_bound)
    ]

    # Sort by combined closeness (price and mileage difference) and return top N
    recommendations['combined_difference'] = (
        abs(recommendations['price'] - input_price) +
        abs(recommendations['mileage'] - input_mileage)
    )
    recommendations = recommendations.sort_values(by='combined_difference').head(top_n)

    return recommendations

# Streamlit App
st.title("Vehicle Recommendation System")
st.subheader("Find the best vehicle recommendations based on cluster, price, and mileage!")

# Upload CSV
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load the dataset
    st.info("Loading data... Please wait for large files.")
    df2 = load_data(uploaded_file)
    
    # Display data preview
    st.write("Dataset Preview")
    st.dataframe(df2.head())

    # Check for necessary columns
    if 'make' in df2.columns and 'price' in df2.columns and 'Cluster' in df2.columns and 'mileage' in df2.columns:
        st.sidebar.header("Input Details")
        
        # Select vehicle make
        input_make = st.sidebar.selectbox("Select Vehicle Make", df2['make'].unique())
        
        # Input price
        input_price = st.sidebar.number_input("Enter Vehicle Price", min_value=0, value=5000, step=100)
        
        # Input mileage
        input_mileage = st.sidebar.number_input("Enter Vehicle Mileage", min_value=0, value=50000, step=1000)
        
        # Recommendation options
        price_tolerance = st.sidebar.slider("Price Tolerance", min_value=500, max_value=10000, value=2000, step=500)
        mileage_tolerance = st.sidebar.slider("Mileage Tolerance", min_value=1000, max_value=20000, value=5000, step=1000)
        top_n = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=20, value=5)

        # Recommendation button
        if st.sidebar.button("Get Recommendations"):
            # Call the recommendation function
            recommendations = recommend_by_cluster_price_and_mileage(
                input_make, input_price, input_mileage, df2, 
                cluster_column='Cluster', price_tolerance=price_tolerance, 
                mileage_tolerance=mileage_tolerance, top_n=top_n
            )
            
            # Display recommendations
            if not recommendations.empty:
                st.write(f"Recommendations for `{input_make}` near price `{input_price}` and mileage `{input_mileage}`:")
                st.dataframe(recommendations)
            else:
                st.warning("No recommendations found within the specified range.")
    else:
        st.error("The dataset must contain 'make', 'price', 'Cluster', and 'mileage' columns.")
else:
    st.info("Please upload a CSV file to begin.")
