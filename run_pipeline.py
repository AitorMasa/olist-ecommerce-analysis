import pandas as pd
from config import RAW,CLEAN,ISSUES
from cleaning import*
from kpi import*
from merge import*

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


#-DATASETS KPI

df_total = pd.read_csv(CLEAN/"total_dataset.csv")
orders_unique = pd.read_csv(CLEAN/"orders_unique.csv")

#-CLEANING---------------

clean_customers(customers) 
clean_geolocation(geolocation) 
clean_items(items) 
clean_payments(payments) 
clean_reviews(reviews) 
clean_orders(orders) 
clean_products(products) 
clean_sellers(sellers) 
clean_category(category) 

#-MERGE---------------

df_total, orders_unique = merge(items, orders,products,sellers,customers,category,reviews,payments)

#-KPI--------------------

mejores_productos(total_dataset)
print("mejores_productos",mejores_productos(df_total))

producto_mas_ventas(total_dataset)
print("producto_mas_ventas",producto_mas_ventas(df_total))

facturacion_evolucion(orders_unique)
print("facturacion_evolucion",facturacion_evolucion(orders_unique))

mejores_clientes(orders_unique)
print("mejores_clientes",mejores_clientes(orders_unique))

ingreso_medio_por_cliente(orders_unique)
print("ingreso_medio_por_cliente",ingreso_medio_por_cliente)

top_20_clientes(orders_unique)
print("top_20_clientes",top_20_clientes(orders_unique))

facturacion_por_estado(total_dataset)
print("facturacion_por_estado",facturacion_por_estado(df_total))

clientes_mas_pedidos(total_dataset)
print("clientes_mas_pedidos",clientes_mas_pedidos(df_total))

operaciones_canceladas(total_dataset)
print("operacionescanceladas",operaciones_canceladas(df_total))

clientes_cancelaciones(total_dataset)
print("clientes_cancelaciones",clientes_cancelaciones(df_total))

print(total_dataset.columns)


