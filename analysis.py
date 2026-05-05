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
SELECT state, SUM(transaction_amount) AS total
FROM aggregated_transaction
GROUP BY state
ORDER BY total DESC
LIMIT 10;
"""


df = pd.read_sql(query, conn)


print(df)


df.plot(kind='bar', x='state', y='total', title="Top 10 States by Transaction Amount")


plt.show()