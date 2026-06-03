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





basic(geolocation)
print(geolocation["geolocation_zip_code_prefix"].value_counts())
mask(geolocation,"geolocation_zip_code_prefix",r"^\d{4,5}$",Issues)
basic_col(geolocation,"geolocation_lat",Issues)
print(geolocation["geolocation_lat"].head())
print(geolocation["geolocation_lng"].head())
geolocation["geolocation_lat"] = pd.to_numeric(geolocation["geolocation_lat"], errors="coerce")

mask_valid = ((geolocation["geolocation_lat"] < 0) &(geolocation["geolocation_lng"] < 0))

print(mask_valid.sum())
print((~mask_valid).sum()) 
lat_numeric = pd.to_numeric(geolocation["geolocation_lat"],errors="coerce")
mask_invalid = lat_numeric.isna()
print(mask_invalid.sum())   
print(geolocation.loc[geolocation["geolocation_lat"]>0])  
print(
    geolocation.loc[
        geolocation["geolocation_lat"] > 0
    ].shape
)
Issues["geolocalizacion_incorrecta"]=geolocation.loc[~mask_valid].copy()