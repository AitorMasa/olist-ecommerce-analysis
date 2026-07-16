import pandas as pd
from config import RAW,CLEAN,ISSUES
from cleaning import*
from kpi import*
from merge import*
from helpers import export_issues

CSV_FILES=["olist_customers_dataset.csv","olist_geolocation_dataset.csv","olist_order_items_dataset.csv",
           "olist_order_payments_dataset.csv","olist_order_reviews_dataset.csv","olist_orders_dataset.csv",
           "olist_products_dataset.csv","olist_sellers_dataset.csv","product_category_name_translation.csv"]

datasets={}

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


#-CLEANING---------------

customers = clean_customers(customers)
geolocation = clean_geolocation(geolocation)
items = clean_items(items)
payments = clean_payments(payments)
reviews = clean_reviews(reviews)
orders = clean_orders(orders)
products = clean_products(products)
sellers = clean_sellers(sellers)
category = clean_category(category)

#-SAVE CLEAN DATASETS--------------

customers.to_csv(CLEAN/"customers_clean.csv", index=False)
geolocation.to_csv(CLEAN/"geolocation_clean.csv", index=False)
items.to_csv(CLEAN/"items_clean.csv", index=False)
payments.to_csv(CLEAN/"payments_clean.csv", index=False)
reviews.to_csv(CLEAN/"reviews_clean.csv", index=False)
products.to_csv(CLEAN/"products_clean.csv", index=False)
orders.to_csv(CLEAN/"orders_clean.csv", index=False)
sellers.to_csv(CLEAN/"sellers_clean.csv", index=False)
category.to_csv(CLEAN/"category_clean.csv", index=False)

#-EXPORT QUALITY ISSUES---------------

export_issues(Issues,ISSUES)


#-MERGE---------------

df_total, orders_unique = merge(items, orders,products,sellers,customers,category,reviews,payments)

#-KPI--------------------


print("mejores_productos")
print(mejores_productos(df_total))

print("producto_mas_ventas")
print(producto_mas_ventas(df_total))

print("facturacion_evolucion")
print(facturacion_evolucion(orders_unique))

print("mejores_clientes")
print(mejores_clientes(orders_unique))

print("ingreso_medio_por_cliente")
print(ingreso_medio_por_cliente(orders_unique))

print("top_20_clientes")
print(top_20_clientes(orders_unique))

print("facturacion_por_estado")
print(facturacion_por_estado(orders_unique))

print("clientes_mas_pedidos")
print(clientes_mas_pedidos(orders_unique))

print("operaciones_canceladas")
print(operaciones_canceladas(orders_unique))

print("clientes_cancelaciones")
print(clientes_cancelaciones(orders_unique))


