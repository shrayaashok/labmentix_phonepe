import os
import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  
    database="phone_pe"
)
cursor = conn.cursor()

transaction_path = "data/data/aggregated/transaction/country/india/state/"

for state in os.listdir(transaction_path):
    state_path = transaction_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                if "data" in data and data["data"] and "transactiondata" in data["data"]:
                    
                    for i in data["data"]["transactiondata"]:
                        name = i["name"]

                        for j in i["paymentinstruments"]:
                            count = j["count"]
                            amount = j["amount"]

                            cursor.execute("""
                            insert into aggregated_transaction
                            values (%s,%s,%s,%s,%s,%s)
                            """, (
                                state,
                                int(year),
                                int(file.strip('.json')),
                                name,
                                count,
                                amount
                            ))

print(" transaction data loaded")


user_path = "data/data/aggregated/user/country/india/state/"

for state in os.listdir(user_path):
    state_path = user_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                
                if (
                    "data" in data and 
                    data["data"] is not None and 
                    "usersbydevice" in data["data"] and 
                    data["data"]["usersbydevice"] is not None
                ):
                    
                    for i in data["data"]["usersbydevice"]:
                        brand = i["brand"]
                        count = i["count"]
                        percentage = i["percentage"]

                        cursor.execute("""
                        insert into aggregated_user
                        values (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            brand,
                            count,
                            percentage
                        ))

print(" user data loaded")


map_path = "data/data/map/transaction/hover/country/india/state/"

for state in os.listdir(map_path):
    state_path = map_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                
                if (
                    "data" in data and 
                    data["data"] is not None and 
                    "hoverdatalist" in data["data"] and 
                    data["data"]["hoverdatalist"] is not None
                ):
                    
                    for i in data["data"]["hoverdatalist"]:
                        district = i["name"]
                        count = i["metric"][0]["count"]
                        amount = i["metric"][0]["amount"]

                        cursor.execute("""
                        insert into map_transaction
                        values (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            district,
                            count,
                            amount
                        ))

print(" map transaction data loaded")


top_path = "data/data/top/transaction/country/india/state/"

for state in os.listdir(top_path):
    state_path = top_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                if (
                    "data" in data and 
                    data["data"] is not None and 
                    "districts" in data["data"] and 
                    data["data"]["districts"] is not None
                ):
                    
                    for i in data["data"]["districts"]:
                        name = i["entityname"]
                        amount = i["metric"]["amount"]
                        count = i["metric"]["count"]

                        cursor.execute("""
                        insert into top_transaction
                        values (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            name,
                            count,
                            amount
                        ))

print(" top transaction data loaded")

conn.commit()
cursor.close()
conn.close()

print(" all data loaded successfully")