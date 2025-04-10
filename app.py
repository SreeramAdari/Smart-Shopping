import streamlit as st
import sqlite3
import pandas as pd
import json

# Connect to the SQLite database
def get_connection():
    return sqlite3.connect("ecommerce_recommendation.db")

# Load customer data
def load_customers():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df

# Load product data
def load_products():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

# Get top 5 recommendations based on category matching (placeholder logic)
def get_recommendations(customer_row, products_df):
    try:
        browse_cats = json.loads(customer_row['Browsing_History'])
        purchase_cats = json.loads(customer_row['Purchase_History'])
    except:
        browse_cats = []
        purchase_cats = []

    matched = products_df[products_df['Category'].isin(browse_cats + purchase_cats)]
    top5 = matched.sort_values(by="Probability_of_Recommendation", ascending=False).head(5)
    return top5

# Load data
customers_df = load_customers()
products_df = load_products()

# Streamlit UI
st.title("🛒 Personalized Product Recommender")
st.markdown("Built with Multi-Agent Architecture")

customer_ids = customers_df['Customer_ID'].tolist()
selected_customer = st.selectbox("Select a Customer ID", customer_ids)

if selected_customer:
    customer_row = customers_df[customers_df['Customer_ID'] == selected_customer].iloc[0]

    st.subheader("Customer Profile")
    st.write({
        "Age": customer_row['Age'],
        "Gender": customer_row['Gender'],
        "Location": customer_row['Location'],
        "Browsing History": json.loads(customer_row['Browsing_History']),
        "Purchase History": json.loads(customer_row['Purchase_History']),
        "Segment": customer_row['Customer_Segment'],
        "Season": customer_row['Season']
    })

    if st.button("🎯 Get Recommendations"):
        recs = get_recommendations(customer_row, products_df)
        st.subheader("Top 5 Recommendations")
        for _, row in recs.iterrows():
            st.markdown(f"**{row['Category']} - {row['Subcategory']}**")
            st.write({
                "Price": row['Price'],
                "Brand": row['Brand'],
                "Rating": row['Product_Rating'],
                "Sentiment Score": row['Customer_Review_Sentiment_Score'],
                "Season": row['Season']
            })
