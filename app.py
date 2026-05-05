import streamlit as st
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="phone_pe"
)

st.title("PhonePe Transaction Insights")

option = st.selectbox(
    "Select Analysis",
    ("Top States", "Payment Types", "Yearly Trend",
     "Top Districts", "Top Brands")
)


if option == "Top States":
    df = pd.read_sql("""
    SELECT state, SUM(transaction_amount) AS total
    FROM aggregated_transaction
    GROUP BY state
    ORDER BY total DESC LIMIT 10
    """, conn)
    st.bar_chart(df.set_index("state"))


elif option == "Payment Types":
    df = pd.read_sql("""
    SELECT transaction_type, SUM(transaction_amount) AS total
    FROM aggregated_transaction
    GROUP BY transaction_type
    """, conn)
    st.bar_chart(df.set_index("transaction_type"))


elif option == "Yearly Trend":
    df = pd.read_sql("""
    SELECT year, SUM(transaction_amount) AS total
    FROM aggregated_transaction
    GROUP BY year
    ORDER BY year
    """, conn)
    st.line_chart(df.set_index("year"))


elif option == "Top Districts":
    df = pd.read_sql("""
    SELECT district, SUM(transaction_amount) AS total
    FROM map_transaction
    GROUP BY district
    ORDER BY total DESC LIMIT 10
    """, conn)
    st.bar_chart(df.set_index("district"))


elif option == "Top Brands":
    df = pd.read_sql("""
    SELECT brand, SUM(user_count) AS total
    FROM aggregated_user
    GROUP BY brand
    ORDER BY total DESC LIMIT 10
    """, conn)
    st.bar_chart(df.set_index("brand"))