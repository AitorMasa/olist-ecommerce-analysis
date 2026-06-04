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


basic(customers)
basic(geolocation)
basic(items)
basic(payments)
basic(reviews)
basic(orders)
basic(products)
basic(sellers)
basic(category)
def clean_customers (df):
    
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

#-------------------
def clean_geolocation (df):
    
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
    print(geolocation.loc[geolocation["geolocation_lat"] > 0].shape)
    Issues["geolocalizacion_incorrecta"]=geolocation.loc[~mask_valid].copy()
    basic_col(geolocation,"geolocation_city",Issues)
    basic_col(geolocation,"geolocation_state",Issues)

#--------------------
def clean_items (df):
    
    basic(items)
    print(items["order_id"].str.len())
    print(items["product_id"].str.len())
    mask(items,"order_id",r"^[a-z0-9]{32}$",Issues)
    mask(items,"product_id",r"^[a-z0-9]{32}$",Issues)
    print(items["order_item_id"].value_counts())
    print((items["order_item_id"]>0).sum())
    print(items["seller_id"].str.len())
    mask(items,"seller_id",r"^[a-z0-9]{32}$",Issues)
    fecha(items,"shipping_limit_date")
    print(items["shipping_limit_date"].describe)
    numeric(items,"price",Issues)
    print(items.loc[items["price"]==6735])
    numeric(items,"freight_value",Issues)

#---------------------
def clean_payments (df):
    
    basic(payments)
    print(payments["order_id"].str.len())
    mask(payments,"order_id",r"^[a-z0-9]{32}$",Issues)
    print(payments["payment_sequential"].value_counts())
    print(payments["payment_type"].count())
    print(payments["payment_type"].value_counts())
    payments_not_defined=payments["payment_type"]=="not_defined"
    Issues["payment_not_defined"]=payments.loc[payments_not_defined].copy()
    numeric(payments,"payment_installments",Issues)
    numeric(payments,"payment_value",Issues)
    zero=(payments["payment_value"]==0).sum()
    print(zero)
    print(payments.loc[payments["payment_value"]==0])
    mask_value_0=payments["payment_value"]==0
    Issues["paument_value_0"]=payments.loc[mask_value_0].copy()

#---------------------
def clean_reviews (reviews):
    
    reviews = reviews.sort_values("review_answer_timestamp")
    reviews = reviews.drop_duplicates(subset="order_id", keep="last")
    print(reviews["review_id"].str.len())
    print(reviews["order_id"].str.len())
    mask(reviews,"review_id",r"^[a-z0-9]{32}$",Issues)
    mask(reviews,"order_id",r"^[a-z0-9]{32}$",Issues)
    numeric(reviews,"review_score",Issues)
    print(reviews["review_score"].value_counts())
    fecha(reviews,"review_creation_date")
    fecha(reviews,"review_answer_timestamp")
    mask_review = (reviews["review_answer_timestamp"] < reviews["review_creation_date"])
    print(mask_review.sum())
    Issues["review_answer_before_creation"] = reviews.loc[mask_review].copy()
    reviews = reviews.loc[~mask_review].copy()


#----------------
def clean_orders (df):
    
    basic(orders)
    print(orders["customer_id"].str.len())
    print(orders["order_id"].str.len())
    mask(orders,"customer_id",r"^[a-z0-9]{32}$",Issues)
    mask(orders,"order_id",r"^[a-z0-9]{32}$",Issues)
    print(orders["order_status"].count())
    print(orders["order_status"].value_counts())
    print(orders["order_status"].isna().sum())
    fecha(orders,"order_purchase_timestamp")
    fecha(orders,"order_approved_at")
    invalid=orders.loc[orders["order_approved_at"].isna()]
    not_valid_aproved=orders["order_approved_at"].isna()
    print(invalid)
    Issues["invalid_order-aproved_data"]=orders.loc[not_valid_aproved].copy()
    fecha(orders,"order_delivered_carrier_date")
    not_valid_carrier_date=orders["order_delivered_carrier_date"].isna()
    Issues["not_valid_carrier_date"]=orders.loc[not_valid_carrier_date].copy()
    fecha(orders,"order_delivered_customer_date")
    not_valid_delivered_customer=orders["order_delivered_customer_date"].isna()
    Issues["not_valid order_delivered_customer_date"]=orders.loc[not_valid_delivered_customer].copy()
    fecha(orders,"order_estimated_delivery_date")

#---------------------
def clean_products (df):
    
    basic(products)
    print(products["product_id"].str.len())
    mask(products,"product_id",r"^[a-z0-9]{32}$",Issues)
    basic_col(products,"product_category_name",Issues)
    print(products.loc[products["product_category_name"].isna()])
    nuls=products["product_category_name"].isna()
    Issues["product_category_null"]=products.loc[nuls].copy()
    basic_col(products,"product_name_lenght",Issues)
    nulos=(products["product_category_name"].isna()
        & products["product_name_lenght"].isna()
        & products["product_description_lenght"].isna()
        & products["product_photos_qty"].isna())
    print(nulos)
    Issues["product_description_null"]=products.loc[nulos].copy()
    numeric(products,"product_weight_g",Issues)
    nuls_weigth=products["product_weight_g"].isna()
    Issues["invalid_product_weight_g"]=products.loc[nuls_weigth].copy()
    numeric(products,"product_weight_g",Issues)
    print(products.loc[products["product_weight_g"]==0])
    incorrect_weigth=products["product_weight_g"]==0
    Issues["invalid_weigth"]=products.loc[incorrect_weigth].copy()
    numeric(products,"product_length_cm",Issues)
    null_legth=products["product_length_cm"].isna()
    Issues["invalid_product_length"]=products.loc[null_legth].copy()
    numeric(products,"product_height_cm",Issues)
    null_heigth=products["product_height_cm"].isna()
    Issues["invalid_product_height"]=products.loc[null_heigth].copy()
    numeric(products,"product_width_cm",Issues)
    null_width=products["product_width_cm"].isna()
    Issues["invalid_product_width"]=products.loc[null_width].copy()


#-------------------
def clean_sellers (df):
    
    basic(sellers)
    print(sellers["seller_id"].str.len())
    mask(sellers,"seller_id",r"^[a-z0-9]{32}$",Issues)
    numeric(sellers,"seller_zip_code_prefix",Issues)
    basic_col(sellers,"seller_city",Issues)
    basic_col(sellers,"seller_state",Issues)

#------------------
def clean_category (df):
    
    basic(category)
    basic_col(category,"product_category_name",Issues)
    basic_col(category,"product_category_name_english",Issues)

#-----------------

export_issues(Issues,ISSUES)

customers.to_csv(CLEAN/"customers_clean.csv", index=False)
geolocation.to_csv(CLEAN/"geolocation_clean.csv", index=False)
items.to_csv(CLEAN/"items_clean.csv", index=False)
payments.to_csv(CLEAN/"payments_clean.csv", index=False)
reviews.to_csv(CLEAN/"reviews_clean.csv", index=False)
products.to_csv(CLEAN/"products_clean.csv", index=False)
orders.to_csv(CLEAN/"orders_clean.csv", index=False)
sellers.to_csv(CLEAN/"sellers_clean.csv", index=False)
category.to_csv(CLEAN/"category_clean.csv", index=False)
