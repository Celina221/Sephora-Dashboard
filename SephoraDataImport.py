import pandas as pd
import mysql.connector
from mysql.connector import Error

#loading CSV
df_products = pd.read_csv("product_info.csv")

#checking columns
print(df_products.columns.tolist())
print(df_products.head())

#Data cleaning
#Drop rows where columns are missing 
df_products = df_products.dropna(subset=["product_name", "brand_name"])


#Fill missing text fields
df_products["highlights"] = df_products["highlights"].fillna("Unknown")

#Price is number not string
df_products["price_usd"] = pd.to_numeric(df_products["price_usd"], errors="coerce")


# Make sure rating is a float
df_products["rating"] = pd.to_numeric(df_products["rating"], errors="coerce")

# Make sure loves_count is integer
df_products["loves_count"] = pd.to_numeric(df_products["loves_count"], errors="coerce").fillna(0).astype(int)


#Check for duplicates and remove
print(f"Duplicate found: {df_products.duplicated().sum()}")
df_products = df_products.drop_duplicates()

#Clean columns
df_products["brand_name"] = df_products["brand_name"].str.strip()
df_products["product_name"] = df_products["product_name"].str.strip()
#df_products["primary_category"] = df_products["primary_category"].str.title()
df_products = df_products.dropna(subset=["product_name", "brand_name", "brand_id"])



#Renaming columns
df_products = df_products.rename(columns={
    "price_usd": "price",
    "loves_count": "loves",
    "sale_price_usd": "sale_price"


})


#column selection
df_clean = df_products[[
    "product_id",
    "product_name",
    "price",
    "loves",
    "reviews",
    "sale_price",
    "out_of_stock",
    "sephora_exclusive",
    "online_only",
    "brand_name",
    "brand_id",
    "rating",
    "size",
    "highlights"
]]

ddf_clean = df_clean.where(pd.notnull(df_clean), None)
df_clean = df_clean.replace({float('nan'): None})
# Replace ALL variations of missing values with None


#Final check
print(f"Cleaned dataset: {df_clean}")
print(df_clean.isnull().sum())


"""Push items to database"""

def push_to_sql(df_clean):
    conn= mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "Sephora_Database"
    )

    cursor= conn.cursor()

    #Insert data for Brand table
    for _, row in df_clean.iterrows():
        cursor.execute("""
                       INSERT IGNORE INTO Brand
                       (brand_id, brand_name)
                       VALUES (%s, %s)""",
                       (
                           row["brand_id"],
                           row["brand_name"]
                         ))

    #insert data for Products table
    for _, row in df_clean.iterrows():
        cursor.execute("""
                       INSERT IGNORE INTO Products
                       (brand_id, product_id, product_name, size,
                       price, sale_price, out_of_stock, sephora_exclusive,
                       online_only)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (
                           row["brand_id"],
                           row["product_id"],
                           row["product_name"],
                           row["size"],
                           row["price"],
                           row["sale_price"],
                           row["out_of_stock"],
                           row["sephora_exclusive"],
                           row["online_only"]
                       ))
        
    #Insert data into Customer_Review table
    for _, row in df_clean.iterrows():
        cursor.execute(
            """INSERT IGNORE INTO Customer_Review
            (product_id, loves, rating, reviews)
            VALUES(%s, %s, %s, %s)""",
            (
                row["product_id"],
                row["loves"],
                row["rating"],
                row["reviews"]
            )
        )
    conn.commit()
    cursor.close()
    conn.close()
    
    print("data successfully pushed to MySQL!")


print(df_clean.columns.tolist())

push_to_sql(df_clean)
