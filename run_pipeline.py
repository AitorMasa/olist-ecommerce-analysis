import pandas as pd
from config import RAW,CLEAN,ISSUES,KPI,CSV_FILES
from cleaning import (clean_customers,clean_geolocation,clean_items,clean_payments,clean_reviews,
                      clean_orders,clean_products,clean_sellers,clean_category)
from kpi import (mejores_productos,producto_mas_ventas,facturacion_evolucion,mejores_clientes,ingreso_medio_por_cliente,
                top_20_clientes,facturacion_por_estado,clientes_mas_pedidos,operaciones_canceladas,clientes_cancelaciones)
from merge import merge
from helpers import export_issues



datasets={}
Issues={}

for file in CSV_FILES:
    nombre=file.replace(".csv","")
    datasets[nombre]=pd.read_csv(RAW/file)

print("[1/7]  Loading raw dataset...")    
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

print("[2/7]  Cleaning dataset...")  
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

print("[3/7]  Saving cleaned datasets...")  
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

print("[4/7]  Exporting issues...")  
export_issues(Issues,ISSUES)


#-MERGE---------------

print("[5/7]  Merging and saving datasets...")  
df_total, orders_unique = merge(items, orders,products,sellers,customers,category,reviews,payments)

df_total.to_csv(CLEAN / "total_dataset.csv", index=False)
orders_unique.to_csv(CLEAN / "orders_unique.csv", index=False)

#-KPI--------------------

print("[6/7]  Calculating  KPIs and saving results...")  
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

resultados_kpi = {
    "mejores_productos": mejores_productos(df_total),
    "producto_mas_ventas": producto_mas_ventas(df_total),
    "facturacion_evolucion": facturacion_evolucion(orders_unique),
    "mejores_clientes": mejores_clientes(orders_unique),
    "ingreso_medio_por_cliente": ingreso_medio_por_cliente(orders_unique),
    "top_20_clientes": top_20_clientes(orders_unique),
    "facturacion_por_estado": facturacion_por_estado(orders_unique),
    "clientes_mas_pedidos": clientes_mas_pedidos(orders_unique),
    "operaciones_canceladas": operaciones_canceladas(orders_unique),
    "clientes_cancelaciones": clientes_cancelaciones(orders_unique),
}


for nombre, resultado in resultados_kpi.items():

    if not isinstance(resultado, pd.DataFrame):
        resultado = pd.DataFrame([resultado])

    resultado.to_csv(KPI / f"{nombre}.csv", index=True)
    
#print("Orders raw:", orders["order_id"].nunique())
#print("Orders unique:", orders_unique["order_id"].nunique())
#print("Items:", len(items))
#print("Total dataset:", len(df_total))

print("[7/7]  Pipeline completed successfully.")  


