import pandas as pd

from config import RAW,CLEAN,ISSUES
from helpers import basic,basic_col,numeric,fecha,mask,export_issues

CSV_FILES=["olist_customers_dataset.csv","olist_geolocation_dataset.csv","olist_order_items_dataset.csv",
           "olist_order_payments_dataset.csv","olist_order_reviews_dataset.csv","olist_orders_dataset.csv",
           "olist_products_dataset.csv","olist_sellers_dataset.csv","product_category_name_translation.csv"]

datasets={}
Issues={}

for file in CSV_FILES:
    nombre=file.replace(".csv","")
    datasets[nombre]=pd.read_csv(RAW/file)
    
customers=datasets["olist_customers_dataset"].copy()
geolocation=datasets["olist_geolocation_dataset"].copy()
#items=datasets["olist_order_items_dataset"].copy() 
#payments=datasets["olist_order_payments_dataset"].copy() 
#reviews=datasets["olist_order_reviews_dataset"].copy() 
#orders=datasets["olist_orders_dataset"].copy() 
#products=datasets["olist_products_dataset"].copy() 
#sellers=datasets["olist_sellers_dataset"].copy()   
#category=datasets["product_category_name_translation"].copy() 


basic(customers)
#basic(geolocation)
#basic(items)
#basic(payments)
#basic(reviews)
#basic(orders)
#basic(products)
#basic(sellers)
#basic(category)

print(customers["customer_id"].str.len())
print(customers["customer_unique_id"].str.len())
mask(customers,"customer_id",r"^[a-z0-9]{32}$",Issues)
mask(customers,"customer_unique_id",r"^[a-z0-9]{32}$",Issues)
print(customers["customer_id"].str.count(r"\d"))
print(customers["customer_id"].str.count(r"[a-z]"))
customers_numeros=customers["customer_id"].str.count(r"\d")
customers_letras=customers["customer_id"].str.count(r"[a-z]")
print(customers_numeros.value_counts())
print(customers_letras.value_counts())
print(customers_numeros.describe())
print(customers_letras.describe())
customers_numeros_unique=customers["customer_unique_id"].str.count(r"\d")
customers_letras_unique=customers["customer_unique_id"].str.count(r"[a-z]")
print(customers_numeros_unique.value_counts())
print(customers_letras_unique.value_counts())
print(customers_numeros_unique.describe())
print(customers_letras_unique.describe())

customers["customer_zip_code_prefix"] = (customers["customer_zip_code_prefix"].astype(str))
mask(customers,"customer_zip_code_prefix",r"^\d{4,5}$",Issues)
customers["customer_zip_code_prefix"].astype(str).str.fullmatch(r"\d{4,5}")
print(customers,"customer_zip_code_prefix")

basic_col(customers,"customer_city",Issues)
basic_col(customers,"customer_state",Issues)



basic(geolocation)
