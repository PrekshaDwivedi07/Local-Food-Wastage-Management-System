import streamlit as st
import pandas as pd
from pandasql import sqldf
import plotly.express as px
import os

# --------------------------
# Page Config & Styling
# --------------------------
st.set_page_config(
    page_title="Food Waste Management Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🍽️"
)

# Custom CSS
st.markdown("""
    <style>
    /* Header Text */
    .header-text {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #1a1a1a !important;   /* Deep charcoal for timeless readability */
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f4f4f4, #e0e0e0);  /* Elegant light grey tones */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }

    /* Metric Card */
    .metric-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); /* Classic navy/charcoal gradient */
        color: #fdfdfd;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Section Header */
    .section-header {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #2c3e50;   /* Navy-charcoal */
        border-left: 5px solid #b8860b;  /* Golden accent */
        padding-left: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


# --------------------------
# Load Data
# --------------------------
@st.cache_data
def load_data():
    base_path = "."
    return {
        "providers": pd.read_csv(os.path.join(base_path, "providers_data.csv")),
        "receivers": pd.read_csv(os.path.join(base_path, "receivers_data.csv")),
        "food": pd.read_csv(os.path.join(base_path, "food_listings_data.csv")),
        "claims": pd.read_csv(os.path.join(base_path, "claims_data.csv"))
    }

data = load_data()
providers_df, receivers_df, food_df, claims_df = (
    data["providers"], data["receivers"], data["food"], data["claims"]
)

# --------------------------
# Run SQL Helper
# --------------------------
def run_query(query):
    tables = {
        "providers_data": providers_df,
        "receivers_data": receivers_df,
        "food_listings_data": food_df,
        "claims_data": claims_df
    }
    try:
        return sqldf(query, tables)
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()

# --------------------------
# Predefined Queries (Your 15)
# --------------------------
predefined_queries = {
    "1. Providers per City": """
        SELECT city, COUNT(*) AS total_providers
        FROM providers_data
        GROUP BY city
        ORDER BY total_providers DESC;
    """,
    "2. Receivers per City": """
        SELECT city, COUNT(*) AS total_receivers
        FROM receivers_data
        GROUP BY city
        ORDER BY total_receivers DESC;
    """,
    "3. Provider Type with Most Listings": """
        SELECT provider_type, COUNT(*) AS total_listings
        FROM food_listings_data
        GROUP BY provider_type
        ORDER BY total_listings DESC;
    """,
    "4. Provider Contacts": """
        SELECT name, contact, city
        FROM providers_data;
    """,
    "5. Receivers with Most Claims": """
        SELECT r.name, COUNT(c.claim_id) AS total_claims
        FROM claims_data c
        JOIN receivers_data r ON c.receiver_id = r.receiver_id
        GROUP BY r.name
        ORDER BY total_claims DESC;
    """,
    "6. Total Food Quantity": """
        SELECT SUM(quantity) AS total_food_quantity
        FROM food_listings_data;
    """,
    "7. City with Highest Listings": """
        SELECT location, COUNT(*) AS total_listings
        FROM food_listings_data
        GROUP BY location
        ORDER BY total_listings DESC
        LIMIT 1;
    """,
    "8. Most Common Food Type": """
        SELECT food_type, COUNT(*) AS type_count
        FROM food_listings_data
        GROUP BY food_type
        ORDER BY type_count DESC
        LIMIT 1;
    """,
    "9. Claims per Food Item": """
        SELECT f.food_name, COUNT(c.claim_id) AS total_claims
        FROM claims_data c
        JOIN food_listings_data f ON c.food_id = f.food_id
        GROUP BY f.food_name
        ORDER BY total_claims DESC
        LIMIT 7;
    """,
    "10. Provider with Most Completed Claims": """
        SELECT p.name, COUNT(c.claim_id) AS successful_claims
        FROM claims_data c
        JOIN food_listings_data f ON c.food_id = f.food_id
        JOIN providers_data p ON f.provider_id = p.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.name
        ORDER BY successful_claims DESC
        LIMIT 1;
    """,
    "11. Claims by Status (%)": """
        SELECT status,
               ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data)),2) AS percentage
        FROM claims_data
        GROUP BY status;
    """,
    "12. Avg Quantity Claimed per Receiver": """
        SELECT r.name, ROUND(AVG(f.quantity), 2) AS avg_quantity_claimed
        FROM claims_data c
        JOIN receivers_data r ON c.receiver_id = r.receiver_id
        JOIN food_listings_data f ON c.food_id = f.food_id
        GROUP BY r.name
        ORDER BY avg_quantity_claimed DESC;
    """,
    "13. Most Claimed Meal Type": """
        SELECT f.meal_type, COUNT(c.claim_id) AS total_claims
        FROM claims_data c
        JOIN food_listings_data f ON c.food_id = f.food_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC;
    """,
    "14. Total Quantity Donated per Provider": """
        SELECT p.name, SUM(f.quantity) AS total_quantity_donated
        FROM food_listings_data f
        JOIN providers_data p ON f.provider_id = p.provider_id
        GROUP BY p.name
        ORDER BY total_quantity_donated DESC;
    """,
    "15. Top 5 Cities by Demand": """
        SELECT f.location AS city, COUNT(c.claim_id) AS total_claims
        FROM claims_data c
        JOIN food_listings_data f ON c.food_id = f.food_id
        GROUP BY f.location
        ORDER BY total_claims DESC
        LIMIT 5;
    """
}

# --------------------------
# Main App
# --------------------------
def main():
    st.markdown('<div class="header-text">🍽️ Food Waste Management Dashboard</div>', unsafe_allow_html=True)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="metric-card"><h3>Total Providers</h3><h1>{len(providers_df)}</h1></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card"><h3>Total Receivers</h3><h1>{len(receivers_df)}</h1></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card"><h3>Food Listings</h3><h1>{len(food_df)}</h1></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card"><h3>Total Claims</h3><h1>{len(claims_df)}</h1></div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2 = st.tabs(["SQL Queries", "Data Explorer"])

    with tab1:
        st.markdown('<div class="section-header">SQL Query Interface</div>', unsafe_allow_html=True)
        selected_query = st.selectbox("Select a query:", list(predefined_queries.keys()))
        if st.button("Run Selected Query"):
            query = predefined_queries[selected_query]
            result = run_query(query)
            st.dataframe(result, use_container_width=True)

    with tab2:
        st.markdown('<div class="section-header">Data Explorer</div>', unsafe_allow_html=True)
        dataset = st.selectbox("Select Dataset:", ["Providers", "Receivers", "Food Listings", "Claims"])
        if dataset == "Providers": st.dataframe(providers_df, use_container_width=True)
        elif dataset == "Receivers": st.dataframe(receivers_df, use_container_width=True)
        elif dataset == "Food Listings": st.dataframe(food_df, use_container_width=True)
        elif dataset == "Claims": st.dataframe(claims_df, use_container_width=True)

if __name__ == "__main__":
    main()

