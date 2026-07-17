import pandas as pd

from config import RAW,CLEAN,ISSUES
from helpers import basic_col,numeric,fecha,mask


Issues={}


def clean_customers (df):
    
   
    mask(df,"customer_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"customer_unique_id",r"^[a-z0-9]{32}$",Issues)

    df_numeros=df["customer_id"].str.count(r"\d")
    df_letras=df["customer_id"].str.count(r"[a-z]")
    df_numeros_unique=df["customer_unique_id"].str.count(r"\d")
    df_letras_unique=df["customer_unique_id"].str.count(r"[a-z]")
    df["customer_zip_code_prefix"] = (df["customer_zip_code_prefix"].astype(str))
    mask(df,"customer_zip_code_prefix",r"^\d{4,5}$",Issues)
    df["customer_zip_code_prefix"].astype(str).str.fullmatch(r"\d{4,5}")
    basic_col(df,"customer_city",Issues)
    basic_col(df,"customer_state",Issues)
    return (df)

#-------------------
def clean_geolocation (df):
    
    
    mask(df,"geolocation_zip_code_prefix",r"^\d{4,5}$",Issues)
    basic_col(df,"geolocation_lat",Issues)
    df["geolocation_lat"] = pd.to_numeric(df["geolocation_lat"], errors="coerce")
    mask_valid = ((df["geolocation_lat"] < 0) &(df["geolocation_lng"] < 0))
    lat_numeric = pd.to_numeric(df["geolocation_lat"],errors="coerce")
    mask_invalid = lat_numeric.isna()
    Issues["geolocalizacion_incorrecta"]=df.loc[~mask_valid].copy()
    basic_col(df,"geolocation_city",Issues)
    basic_col(df,"geolocation_state",Issues)
    return (df)

#--------------------
def clean_items (df):
    
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"product_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"seller_id",r"^[a-z0-9]{32}$",Issues)
    fecha(df,"shipping_limit_date")
    numeric(df,"price",Issues)
    numeric(df,"freight_value",Issues)
    return df

#---------------------
def clean_payments (df):
    
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    payments_not_defined=df["payment_type"]=="not_defined"
    Issues["payment_not_defined"]=df.loc[payments_not_defined].copy()
    numeric(df,"payment_installments",Issues)
    numeric(df,"payment_value",Issues)
    zero=(df["payment_value"]==0).sum()
    mask_value_0=df["payment_value"]==0
    Issues["payment_value_0"]=df.loc[mask_value_0].copy()
    return df

#---------------------
def clean_reviews (df):
    
    df = df.sort_values("review_answer_timestamp")
    df = df.drop_duplicates(subset="order_id", keep="last")
    mask(df,"review_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    numeric(df,"review_score",Issues)
    fecha(df,"review_creation_date")
    fecha(df,"review_answer_timestamp")
    mask_review = (df["review_answer_timestamp"] < df["review_creation_date"])
    Issues["review_answer_before_creation"] = df.loc[mask_review].copy()
    df = df.loc[~mask_review].copy()
    return (df)


#----------------
def clean_orders (df):
   
    mask(df,"customer_id",r"^[a-z0-9]{32}$",Issues)
    mask(df,"order_id",r"^[a-z0-9]{32}$",Issues)
    invalid=df.loc[df["order_approved_at"].isna()]
    not_valid_aproved=df["order_approved_at"].isna()
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
    
    mask(df,"product_id",r"^[a-z0-9]{32}$",Issues)
    basic_col(df,"product_category_name",Issues)
    nuls=df["product_category_name"].isna()
    Issues["product_category_null"]=df.loc[nuls].copy()
    basic_col(df,"product_name_lenght",Issues)
    nulos=(df["product_category_name"].isna()
        & df["product_name_lenght"].isna()
        & df["product_description_lenght"].isna()
        & df["product_photos_qty"].isna())
    Issues["product_description_null"]=df.loc[nulos].copy()
    numeric(df,"product_weight_g",Issues)
    nuls_weigth=df["product_weight_g"].isna()
    Issues["invalid_product_weight_g"]=df.loc[nuls_weigth].copy()
    numeric(df,"product_weight_g",Issues)
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
    
    mask(df,"seller_id",r"^[a-z0-9]{32}$",Issues)
    numeric(df,"seller_zip_code_prefix",Issues)
    return (df)

#------------------
def clean_category (df):
    
    basic_col(df,"product_category_name",Issues)
    basic_col(df,"product_category_name_english",Issues)
    return (df)



