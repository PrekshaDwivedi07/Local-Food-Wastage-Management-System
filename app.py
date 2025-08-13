import streamlit as st
import mysql.connector
import pandas as pd

# --------------------------
# Database connection setup
# --------------------------
st.set_page_config(page_title="Local Food Waste Management", layout="wide")
st.title(" Local Food Waste Management Dashboard")

# Sidebar for DB credentials
st.sidebar.header("Database Connection")
db_host = st.sidebar.text_input("Host", "localhost")
db_user = st.sidebar.text_input("User", "root")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database", "Food_wastage")

if st.sidebar.button("Connect to Database"):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        st.success(" Connected to Database!")
        
        # List of queries from your SQL file
        queries = {
            "Providers per City": """
                SELECT city , COUNT(*) AS total_providers
                FROM providers_data
                GROUP BY city
                ORDER BY total_providers DESC;
            """,
            "Receivers per City": """
                SELECT City, COUNT(*) AS total_receivers
                FROM receivers_data
                GROUP BY City
                ORDER BY total_receivers DESC;
            """,
            "Top Provider Type": """
                SELECT Provider_Type, COUNT(*) AS food_listing
                FROM food_listings_data
                GROUP BY Provider_Type
                ORDER BY food_listing DESC
                LIMIT 1;
            """,
            "Top Receiver by Claims": """
                SELECT r.name, COUNT(c.claim_id) AS total_claims
                FROM claims_data c
                JOIN receivers_data r ON c.receiver_id = r.receiver_id
                GROUP BY r.name
                ORDER BY total_claims DESC;
            """,
            "Most Common Food Type": """
                SELECT Food_Type , COUNT(*) AS COUNT_OF_TYPE
                FROM food_listings_data 
                GROUP BY Food_Type
                ORDER BY COUNT_OF_TYPE DESC
                LIMIT 1;
            """,
            "Claims by Status (%)": """
                SELECT status,
                       ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data)), 2) AS percentage
                FROM claims_data
                GROUP BY status;
            """,
            "Top 5 Cities by Demand": """
                SELECT f.location AS city, COUNT(c.claim_id) AS total_claims
                FROM claims_data c
                JOIN food_listings_data f ON c.food_id = f.food_id
                GROUP BY f.location
                ORDER BY total_claims DESC
                LIMIT 5;
            """
        }

        # Execute and display each query
        for title, query in queries.items():
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            st.subheader(title)
            st.dataframe(df)

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")
