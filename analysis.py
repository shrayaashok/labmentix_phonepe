import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",   
    database="phone_pe"
)

query = """
select state, sum(transaction_amount) as total
from aggregated_transaction
group by state
order by total desc
limit 10;
"""
df = pd.read_sql(query, conn)

print(df)

df.plot(kind='bar', x='state', y='total', title="top 10 states by transaction amount")

plt.show()