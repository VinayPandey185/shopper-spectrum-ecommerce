import streamlit as st
import pickle
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Shopper Spectrum", page_icon="🛒", layout="wide")

# -----------------------------
# Load Models
# -----------------------------
kmeans = pickle.load(open("models/kmeans.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))
segment_mapping = pickle.load(open("models/segment_mapping.pkl", "rb"))

product_similarity = pickle.load(open("models/product_similarity.pkl", "rb"))

product_list = pickle.load(open("models/product_list.pkl", "rb"))

feature_columns = pickle.load(open("models/feature_columns.pkl", "rb"))


# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.title("🛒 Shopper Spectrum")

page = st.sidebar.radio(
    "Navigation", ["Home", "Customer Segmentation", "Product Recommendation"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "Home":

    st.title("🛒 Shopper Spectrum")

    st.subheader("Customer Segmentation & Product Recommendation System")

    st.markdown("""
    This application helps businesses:

    - Identify customer segments
    - Predict customer category
    - Recommend similar products
    - Improve marketing strategies
    """)

    st.markdown("""
    Analyze customer behavior, identify valuable customer segments,
    and recommend similar products using Machine Learning.
    """)

    st.markdown("---")

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="👥 Customers", value="4,338")

    with col2:
        st.metric(label="🛍 Products", value="3,877")

    with col3:
        st.metric(label="📦 Transactions", value="397,884")

    st.markdown("---")

    # Features
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Customer Segmentation")

        st.markdown("""
        Identify customer groups based on:

        - High-Value Customers
        - Regular Customers
        - Occasional Customers
        - At-Risk Customers

        Uses RFM Analysis and K-Means Clustering.
        """)

    with c2:
        st.subheader("🛍 Product Recommendation")

        st.markdown("""
        Recommend similar products using:

        - Item-Based Collaborative Filtering
        - Cosine Similarity
        - Customer Purchase History

        Returns Top 5 Similar Products.
        """)

    st.markdown("---")

    st.subheader("📈 Customer Segment Distribution")

    segment_counts = {
        "At-Risk": 1612,
        "Regular": 1173,
        "Occasional": 837,
        "High-Value": 716,
    }

    segment_df = pd.DataFrame(
        {
            "Segment": list(segment_counts.keys()),
            "Customers": list(segment_counts.values()),
        }
    )

    st.bar_chart(segment_df.set_index("Segment"))
# -----------------------------
# Customer Segmentation
# -----------------------------
elif page == "Customer Segmentation":

    st.header("📊 Customer Segmentation")

    recency = st.number_input("Recency (Days)", min_value=1, value=30)

    frequency = st.number_input("Frequency (Purchases)", min_value=1, value=5)

    monetary = st.number_input("Monetary (Total Spend)", min_value=1.0, value=1000.0)

    if st.button("Predict Segment"):

        import pandas as pd
        import numpy as np

        # Create DataFrame
        input_data = pd.DataFrame(
            {"Recency": [recency], "Frequency": [frequency], "Monetary": [monetary]}
        )

        # Apply same log transformation used during training
        input_data = np.log1p(input_data)

        # Scale
        scaled_data = scaler.transform(input_data)

        # Predict Cluster
        cluster = kmeans.predict(scaled_data)[0]

        # Convert cluster to segment
        segment = segment_mapping[cluster]

        st.success(f"Predicted Customer Segment: {segment}")
# -----------------------------
# Product Recommendation
# -----------------------------
elif page == "Product Recommendation":

    st.header("🛍 Product Recommendation")

    selected_product = st.selectbox("Select Product", sorted(product_list))

    if st.button("Get Recommendations"):

        similar_scores = product_similarity[selected_product].sort_values(
            ascending=False
        )

        recommendations = similar_scores.iloc[1:6].index.tolist()

        st.subheader("Recommended Products")

        for product in recommendations:
            st.success(product)
