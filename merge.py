import pandas as pd

from config import CLEAN

customers=pd.read_csv(CLEAN/"customers_clean.csv")
geolocation=pd.read_csv(CLEAN/"geolocation_clean.csv")
items=pd.read_csv(CLEAN/"items_clean.csv")
payments=pd.read_csv(CLEAN/"payments_clean.csv")
reviews=pd.read_csv(CLEAN/"reviews_clean.csv") 
products=pd.read_csv(CLEAN/"products_clean.csv" )
orders=pd.read_csv(CLEAN/"orders_clean.csv" )
sellers=pd.read_csv(CLEAN/"sellers_clean.csv" )
category=pd.read_csv(CLEAN/"category_clean.csv")

def merge(items, orders,products,sellers,customers,category,reviews,payments):
    print(items.shape)
    df_total=items.merge(
        orders,
        on="order_id",
        how="left"
    )
    print(df_total.shape)

    df_total=df_total.merge(
        products,
        on="product_id",
        how="left"
    )
    print(df_total.shape)

    df_total=df_total.merge(
        sellers,
        on="seller_id",
        how="left"
    )
    print(df_total.shape)

    df_total=df_total.merge(
        customers,
        on="customer_id",
        how="left"
    )
    print(df_total.shape)

    df_total=df_total.merge(
        category,
        on="product_category_name",
        how="left"
    )
    print(df_total.shape)
    reviews_agg = (
        reviews
        .sort_values("review_answer_timestamp")
        .groupby("order_id")
        .last()
        .reset_index()
    )
    df_total=df_total.merge(
        reviews_agg,
        on="order_id",
        how="left"
    )
    print(df_total.shape)

    payments_agg = payments.groupby("order_id").agg(
        payment_total=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
        payment_count=("payment_sequential", "count"),
        payment_type=("payment_type", "last")
    ).reset_index()

    df_total=df_total.merge(
        payments_agg,
        on="order_id",
        how="left"
    )
    print(df_total.shape)

    orders_unique = (df_total.groupby("order_id").first().reset_index())
    df_total.to_csv(CLEAN/"total_dataset.csv",index=False)
    orders_unique.to_csv(CLEAN / "orders_unique.csv",index=False)
    
    return df_total, orders_unique

print(payments["payment_value"].dtype)

print(payments["payment_value"].describe())

print(
    payments["payment_value"]
    .sort_values()
    .head(20)
)

print(
    payments["payment_value"]
    .sort_values(ascending=False)
    .head(20)
)

                 
