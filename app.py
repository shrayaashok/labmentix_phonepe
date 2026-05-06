import streamlit as st
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="phone_pe"
)

st.title("phonepe transaction insights")

option = st.selectbox(
    "select analysis",
    ("top states", "payment types", "yearly trend",
     "top districts", "top brands")
)

if option == "top states":
    df = pd.read_sql("""
    select state, sum(transaction_amount) as total
    from aggregated_transaction
    group by state
    order by total desc limit 10
    """, conn)
    st.bar_chart(df.set_index("state"))

elif option == "payment types":
    df = pd.read_sql("""
    select transaction_type, sum(transaction_amount) as total
    from aggregated_transaction
    group by transaction_type
    """, conn)
    st.bar_chart(df.set_index("transaction_type"))

elif option == "yearly trend":
    df = pd.read_sql("""
    select year, sum(transaction_amount) as total
    from aggregated_transaction
    group by year
    order by year
    """, conn)
    st.line_chart(df.set_index("year"))

elif option == "top districts":
    df = pd.read_sql("""
    select district, sum(transaction_amount) as total
    from map_transaction
    group by district
    order by total desc limit 10
    """, conn)
    st.bar_chart(df.set_index("district"))


elif option == "top brands":
    df = pd.read_sql("""
    select brand, sum(user_count) as total
    from aggregated_user
    group by brand
    order by total desc limit 10
    """, conn)
    st.bar_chart(df.set_index("brand"))