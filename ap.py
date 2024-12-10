import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Vehicle Recommendation System",
    layout="wide",  # Wide layout for better visuals
    initial_sidebar_state="expanded"
)

# Main Title
st.title("🚘 Vehicle Recommendation System")
st.markdown("""
Welcome to the **Vehicle Recommendation System**! 
This app recommends the best vehicles based on user input. Even if no exact matches are found, 
we’ll provide fallback recommendations to ensure you always get results.
""")

# Sidebar for navigation
st.sidebar.header("🔧 Controls")
st.sidebar.info("Use the controls below to interact with the application.")

# Load data function
@st.cache_data
def load_data(file):
    """Load the dataset and cache it for performance."""
    return pd.read_csv(file)

# Recommendation function
@st.cache_data
def recommend_by_cluster_price_and_mileage(input_make, input_price, input_mileage, df, cluster_column='Cluster', price_tolerance=2000, mileage_tolerance=5000, top_n=5):
    """Recommend vehicles efficiently."""
    input_cluster = df[df['make'] == input_make][cluster_column].iloc[0]
    cluster_data = df[df[cluster_column] == input_cluster]
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
    recommendations['combined_difference'] = (
        abs(recommendations['price'] - input_price) +
        abs(recommendations['mileage'] - input_mileage)
    )
    return recommendations.sort_values(by='combined_difference').head(top_n)

# Upload Data
st.sidebar.header("📤 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    st.sidebar.success("📂 File uploaded successfully!")
    df = load_data(uploaded_file)

    st.write("### Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Check if necessary columns are present
    if {'make', 'price', 'Cluster', 'mileage', 'stock_type'}.issubset(df.columns):
        # Input Section
        st.sidebar.header("📊 Input Parameters")
        input_make = st.sidebar.selectbox("Select Vehicle Make", df['make'].unique())
        input_price = st.sidebar.number_input("Enter Vehicle Price ($)", min_value=0, value=20000, step=1000)
        input_mileage = st.sidebar.number_input("Enter Vehicle Mileage (km)", min_value=0, value=50000, step=1000)
        price_tolerance = st.sidebar.slider("Price Tolerance ($)", min_value=500, max_value=10000, value=2000, step=500)
        mileage_tolerance = st.sidebar.slider("Mileage Tolerance (km)", min_value=1000, max_value=20000, value=5000, step=1000)
        top_n = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=20, value=5)

        # Get Recommendations
        if st.sidebar.button("💡 Get Recommendations"):
            recommendations = recommend_by_cluster_price_and_mileage(
                input_make, input_price, input_mileage, df,
                cluster_column='Cluster', price_tolerance=price_tolerance,
                mileage_tolerance=mileage_tolerance, top_n=top_n
            )

            # Check recommendations
            if recommendations.empty:
                st.warning("No exact matches found. Expanding search criteria...")

                # Step 1: Loosen tolerances
                expanded_recommendations = df[
                    (df['price'] >= input_price - 2 * price_tolerance) &
                    (df['price'] <= input_price + 2 * price_tolerance) &
                    (df['mileage'] >= input_mileage - 2 * mileage_tolerance) &
                    (df['mileage'] <= input_mileage + 2 * mileage_tolerance)
                ]

                # Step 2: Compute 'combined_difference' for expanded dataset
                if not expanded_recommendations.empty:
                    expanded_recommendations['combined_difference'] = (
                        abs(expanded_recommendations['price'] - input_price) +
                        abs(expanded_recommendations['mileage'] - input_mileage)
                    )
                    expanded_recommendations = expanded_recommendations.sort_values(by='combined_difference').head(top_n)
                    st.success("Here are matches with expanded tolerances:")
                    st.dataframe(expanded_recommendations)
                else:
                    # Step 3: Fallback - Show top cars from the dataset
                    st.warning("Still no matches found. Showing general recommendations:")
                    fallback_recommendations = df.copy()

                    # Calculate 'combined_difference' for the full dataset
                    fallback_recommendations['combined_difference'] = (
                        abs(fallback_recommendations['price'] - input_price) +
                        abs(fallback_recommendations['mileage'] - input_mileage)
                    )
                    fallback_recommendations = fallback_recommendations.sort_values(by='combined_difference').head(top_n)
                    st.dataframe(fallback_recommendations)
            else:
                # Show strict recommendations
                st.subheader("📋 Recommendations (Strict Criteria)")
                st.markdown(f"### Recommendations for `{input_make}` near price `${input_price}` and mileage `{input_mileage}`:")
                st.dataframe(recommendations)
    else:
        st.error("⚠️ The dataset must contain the columns: 'make', 'price', 'Cluster', 'mileage', and 'stock_type'.")
else:
    st.warning("📥 Upload a CSV file to start!")

# Footer Section
st.markdown("---")
st.markdown("""
#### Developed for better vehicle insights and smarter recommendations.
This app is powered by **Streamlit** and designed for better decision-making in the automotive industry. 🚀
""")
