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

def clean_customers (df):
    
    basic(df)
    print(df["customer_id"].str.len())
    print(df["customer_unique_id"].str.len())
    mask(df,"customer_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"customer_unique_id",r"^[a-z0-9]{32}$",Issues)
    print(df["customer_id"].str.count(r"\d"))
    print(df["customer_id"].str.count(r"[a-z]"))
    df_numeros=df["customer_id"].str.count(r"\d")
    df_letras=df["customer_id"].str.count(r"[a-z]")
    print(df_numeros.value_counts())
    print(df_letras.value_counts())
    print(df_numeros.describe())
    print(df_letras.describe())
    df_numeros_unique=df["customer_unique_id"].str.count(r"\d")
    df_letras_unique=df["customer_unique_id"].str.count(r"[a-z]")
    print(df_numeros_unique.value_counts())
    print(df_letras_unique.value_counts())
    print(df_numeros_unique.describe())
    print(df_letras_unique.describe())

    df["customer_zip_code_prefix"] = (df["customer_zip_code_prefix"].astype(str))
    mask(df,"customer_zip_code_prefix",r"^\d{4,5}$",Issues)
    df["customer_zip_code_prefix"].astype(str).str.fullmatch(r"\d{4,5}")
    print(df,"customer_zip_code_prefix")

    basic_col(df,"customer_city",Issues)
    basic_col(df,"customer_state",Issues)
    return (df)

#-------------------
def clean_geolocation (df):
    
    basic(df)
    print(df["geolocation_zip_code_prefix"].value_counts())
    mask(df,"geolocation_zip_code_prefix",r"^\d{4,5}$",Issues)
    basic_col(df,"geolocation_lat",Issues)
    print(df["geolocation_lat"].head())
    print(df["geolocation_lng"].head())
    df["geolocation_lat"] = pd.to_numeric(df["geolocation_lat"], errors="coerce")
    mask_valid = ((df["geolocation_lat"] < 0) &(df["geolocation_lng"] < 0))
    print(mask_valid.sum())
    print((~mask_valid).sum()) 
    lat_numeric = pd.to_numeric(df["geolocation_lat"],errors="coerce")
    mask_invalid = lat_numeric.isna()
    print(mask_invalid.sum())   
    print(df.loc[df["geolocation_lat"]>0])  
    print(df.loc[df["geolocation_lat"] > 0].shape)
    Issues["geolocalizacion_incorrecta"]=df.loc[~mask_valid].copy()
    basic_col(df,"geolocation_city",Issues)
    basic_col(df,"geolocation_state",Issues)
    return (df)

#--------------------
def clean_items (df):
    
    basic(df)
    print(df["order_id"].str.len())
    print(df["product_id"].str.len())
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"product_id",r"^[a-z0-9]{32}$",Issues)
    print(df["order_item_id"].value_counts())
    print((df["order_item_id"]>0).sum())
    print(df["seller_id"].str.len())
    mask(df,"seller_id",r"^[a-z0-9]{32}$",Issues)
    fecha(df,"shipping_limit_date")
    print(df["shipping_limit_date"].describe)
    numeric(df,"price",Issues)
    print(df.loc[df["price"]==6735])
    numeric(df,"freight_value",Issues)
    return df

#---------------------
def clean_payments (df):
    
    basic(df)
    print(df["order_id"].str.len())
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    print(df["payment_sequential"].value_counts())
    print(df["payment_type"].count())
    print(df["payment_type"].value_counts())
    payments_not_defined=df["payment_type"]=="not_defined"
    Issues["payment_not_defined"]=df.loc[payments_not_defined].copy()
    numeric(df,"payment_installments",Issues)
    numeric(df,"payment_value",Issues)
    zero=(df["payment_value"]==0).sum()
    print(zero)
    print(df.loc[df["payment_value"]==0])
    mask_value_0=df["payment_value"]==0
    Issues["payment_value_0"]=df.loc[mask_value_0].copy()
    return df

#---------------------
def clean_reviews (df):
    
    basic(df)
    df = df.sort_values("review_answer_timestamp")
    df = df.drop_duplicates(subset="order_id", keep="last")
    print(df["review_id"].str.len())
    print(df["order_id"].str.len())
    mask(df,"review_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    numeric(df,"review_score",Issues)
    print(df["review_score"].value_counts())
    fecha(df,"review_creation_date")
    fecha(df,"review_answer_timestamp")
    mask_review = (df["review_answer_timestamp"] < df["review_creation_date"])
    print(mask_review.sum())
    Issues["review_answer_before_creation"] = df.loc[mask_review].copy()
    df = df.loc[~mask_review].copy()
    return (df)


#----------------
def clean_orders (df):
    
    basic(df)
    print(df["customer_id"].str.len())
    print(df["order_id"].str.len())
    mask(df,"customer_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    print(df["order_status"].count())
    print(df["order_status"].value_counts())
    print(df["order_status"].isna().sum())
    fecha(df,"order_purchase_timestamp")
    fecha(df,"order_approved_at")
    invalid=df.loc[df["order_approved_at"].isna()]
    not_valid_aproved=df["order_approved_at"].isna()
    print(invalid)
    Issues["invalid_order-aproved_data"]=df.loc[not_valid_aproved].copy()
    fecha(df,"order_delivered_carrier_date")
    not_valid_carrier_date=df["order_delivered_carrier_date"].isna()
    Issues["not_valid_carrier_date"]=df.loc[not_valid_carrier_date].copy()
    fecha(df,"order_delivered_customer_date")
    not_valid_delivered_customer=df["order_delivered_customer_date"].isna()
    Issues["not_valid order_delivered_customer_date"]=df.loc[not_valid_delivered_customer].copy()
    fecha(df,"order_estimated_delivery_date")
    return (df)

#---------------------
def clean_products (df):
    
    basic(df)
    print(df["product_id"].str.len())
    mask(df,"product_id",r"^[a-z0-9]{32}$",Issues)
    basic_col(df,"product_category_name",Issues)
    print(df.loc[df["product_category_name"].isna()])
    nuls=df["product_category_name"].isna()
    Issues["product_category_null"]=df.loc[nuls].copy()
    basic_col(df,"product_name_lenght",Issues)
    nulos=(df["product_category_name"].isna()
        & df["product_name_lenght"].isna()
        & df["product_description_lenght"].isna()
        & df["product_photos_qty"].isna())
    print(nulos)
    Issues["product_description_null"]=df.loc[nulos].copy()
    numeric(df,"product_weight_g",Issues)
    nuls_weigth=df["product_weight_g"].isna()
    Issues["invalid_product_weight_g"]=df.loc[nuls_weigth].copy()
    numeric(df,"product_weight_g",Issues)
    print(df.loc[df["product_weight_g"]==0])
    incorrect_weigth=df["product_weight_g"]==0
    Issues["invalid_weigth"]=df.loc[incorrect_weigth].copy()
    numeric(df,"product_length_cm",Issues)
    null_legth=df["product_length_cm"].isna()
    Issues["invalid_product_length"]=df.loc[null_legth].copy()
    numeric(df,"product_height_cm",Issues)
    null_heigth=df["product_height_cm"].isna()
    Issues["invalid_product_height"]=df.loc[null_heigth].copy()
    numeric(df,"product_width_cm",Issues)
    null_width=df["product_width_cm"].isna()
    Issues["invalid_product_width"]=df.loc[null_width].copy()
    return (df)

#-------------------
def clean_sellers (df):
    
    basic(df)
    print(df["seller_id"].str.len())
    mask(df,"seller_id",r"^[a-z0-9]{32}$",Issues)
    numeric(df,"seller_zip_code_prefix",Issues)
    basic_col(df,"seller_city",Issues)
    basic_col(df,"seller_state",Issues)
    return (df)

#------------------
def clean_category (df):
    
    basic(df)
    basic_col(df,"product_category_name",Issues)
    basic_col(df,"product_category_name_english",Issues)
    return (df)



 