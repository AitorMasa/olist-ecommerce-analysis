import pandas as pd
from config import CLEAN

def merge(items, orders,products,sellers,customers,category,reviews,payments):
    #print(items.shape)
    df_total=items.merge(
        orders,
        on="order_id",
        how="left"
    )
    #print(df_total.shape)

    df_total=df_total.merge(
        products,
        on="product_id",
        how="left"
    )
    #print(df_total.shape)

    df_total=df_total.merge(
        sellers,
        on="seller_id",
        how="left"
    )
    #print(df_total.shape)

    df_total=df_total.merge(
        customers,
        on="customer_id",
        how="left"
    )
    #print(df_total.shape)

    df_total=df_total.merge(
        category,
        on="product_category_name",
        how="left"
    )
    #print(df_total.shape)
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
   # print(df_total.shape)

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
    #print(df_total.shape)

    orders_unique = (
    orders
    .merge(
        customers,
        on="customer_id",
        how="left"
    )
    .merge(
        payments_agg,
        on="order_id",
        how="left"
    )
    .merge(
        reviews_agg,
        on="order_id",
        how="left"
    )
)
    df_total.to_csv(CLEAN/"total_dataset.csv",index=False)
    orders_unique.to_csv(CLEAN / "orders_unique.csv",index=False)
    
    return df_total, orders_unique



                 
