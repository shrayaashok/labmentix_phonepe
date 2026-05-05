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

                if "data" in data and data["data"] and "transactionData" in data["data"]:
                    
                    for i in data["data"]["transactionData"]:
                        name = i["name"]

                        for j in i["paymentInstruments"]:
                            count = j["count"]
                            amount = j["amount"]

                            cursor.execute("""
                            INSERT INTO aggregated_transaction
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """, (
                                state,
                                int(year),
                                int(file.strip('.json')),
                                name,
                                count,
                                amount
                            ))

print("✅ Transaction Data Loaded")

# ---------------- USER DATA LOADING (FIXED) ----------------

user_path = "data/data/aggregated/user/country/india/state/"

for state in os.listdir(user_path):
    state_path = user_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                # ✅ SAFE CHECK (IMPORTANT)
                if (
                    "data" in data and 
                    data["data"] is not None and 
                    "usersByDevice" in data["data"] and 
                    data["data"]["usersByDevice"] is not None
                ):
                    
                    for i in data["data"]["usersByDevice"]:
                        brand = i["brand"]
                        count = i["count"]
                        percentage = i["percentage"]

                        cursor.execute("""
                        INSERT INTO aggregated_user
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            brand,
                            count,
                            percentage
                        ))

print("✅ User Data Loaded")

# =========================================================
# 🔹 3. LOAD MAP TRANSACTION DATA (DISTRICT LEVEL)
# =========================================================

map_path = "data/data/map/transaction/hover/country/india/state/"

for state in os.listdir(map_path):
    state_path = map_path + state + "/"
    
    for year in os.listdir(state_path):
        year_path = state_path + year + "/"
        
        for file in os.listdir(year_path):
            file_path = year_path + file
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                # ✅ SAFE CHECK
                if (
                    "data" in data and 
                    data["data"] is not None and 
                    "hoverDataList" in data["data"] and 
                    data["data"]["hoverDataList"] is not None
                ):
                    
                    for i in data["data"]["hoverDataList"]:
                        district = i["name"]
                        count = i["metric"][0]["count"]
                        amount = i["metric"][0]["amount"]

                        cursor.execute("""
                        INSERT INTO map_transaction
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            district,
                            count,
                            amount
                        ))

print("✅ Map Transaction Data Loaded")

# =========================================================
# 🔹 4. LOAD TOP TRANSACTION DATA
# =========================================================

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
                        name = i["entityName"]
                        amount = i["metric"]["amount"]
                        count = i["metric"]["count"]

                        cursor.execute("""
                        INSERT INTO top_transaction
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """, (
                            state,
                            int(year),
                            int(file.strip('.json')),
                            name,
                            count,
                            amount
                        ))

print("✅ Top Transaction Data Loaded")

conn.commit()
cursor.close()
conn.close()

print("🎉 ALL DATA LOADED SUCCESSFULLY")