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
items=datasets["olist_order_items_dataset"].copy() 
payments=datasets["olist_order_payments_dataset"].copy() 
reviews=datasets["olist_order_reviews_dataset"].copy() 
orders=datasets["olist_orders_dataset"].copy() 
products=datasets["olist_products_dataset"].copy() 
sellers=datasets["olist_sellers_dataset"].copy()   
category=datasets["product_category_name_translation"].copy()
 

pd.set_option("display.max_columns", None)

print(payments["order_id"].nunique())
print(payments["order_id"].duplicated().sum())
print(payments.loc[payments["order_id"].duplicated()])
print(payments.loc[payments["order_id"]=="683bf306149bb869980b68d48a1bd6ab"])
print(payments.loc[payments["order_id"]=="2cbcb371aee438c59b722a21d83597e0"])
print(payments.loc[payments["order_id"]=="31bc09fdbd701a7a4f9b55b5955b8687"])

print(
    total_dataset["payment_total"].sum())   