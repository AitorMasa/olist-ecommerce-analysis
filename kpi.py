import pandas as pd
from config import CLEAN

CSV_FILES = "total_dataset.csv"

total_dataset=pd.read_csv(CLEAN / "total_dataset.csv")

dataset={}

# ¿Cómo ha evolucionado la facturación mes a mes?

print(total_dataset.columns)

total_dataset["order_purchase_timestamp"]=pd.to_datetime(total_dataset["order_purchase_timestamp"],format="mixed",errors="coerce",dayfirst="true")
total_dataset["order_purchase_timestamp_month"]=total_dataset["order_purchase_timestamp"].dt.month
total_dataset["order_purchase_timestamp_y_m"]=(total_dataset["order_purchase_timestamp"].dt.to_period("M"))

facturacion_mensual=total_dataset.groupby("order_purchase_timestamp_y_m").agg(
    facturacion=("payment_total","sum")
).sort_index
print(facturacion_mensual)
print(total_dataset["order_purchase_timestamp"].max())
print(total_dataset[total_dataset["order_purchase_timestamp_y_m"] == "2018-09"])
mask=total_dataset["order_id"]=="54282e97f61c23b78330c15b154c867d"
print(total_dataset.loc[mask, ["order_id", "order_purchase_timestamp","payment_total","payment_installments"]])
mask = total_dataset["order_purchase_timestamp"].dt.year == 2016

print(total_dataset.loc[ mask, "order_purchase_timestamp"].sort_values())
print(print(total_dataset.loc[mask,"order_purchase_timestamp_y_m"].value_counts().sort_index()))

mask = (total_dataset["order_purchase_timestamp"].dt.year == 2018) & (total_dataset["order_purchase_timestamp"].dt.month==3)

print(total_dataset.loc[mask,["order_id", "order_purchase_timestamp","payment_total","payment_installments"]])


# ¿Qué productos generan más ingresos para la empresa?

print(total_dataset.columns)

prod=total_dataset.groupby("product_id").agg(
    price_total=("price","sum")
).sort_values(by="price_total",ascending=False)
print("prodcutos que mas ingresos genera:",prod)
print(total_dataset["product_id"].count())
print(total_dataset["product_id"].nunique())
print(total_dataset["product_id"].value_counts())

#  KPI 3 ¿Qué clientes generan más ingresos para la empresa?
cli=total_dataset.groupby("customer_unique_id").agg(
    price=("price","sum")
).sort_values(by="price",ascending=False)
print("cliente que mas ingresos genera",cli)

print(total_dataset["customer_id"].nunique())
print(total_dataset["customer_unique_id"].nunique())


# ¿Qué Facturación por estado la empresa?
estado=total_dataset.groupby("customer_state").agg(
    price=("price","sum")
).sort_values(by="price",ascending=False)
print("estado que mas facturacion genera:", estado)

# ¿¿Cuánto gasta de media un cliente en cada compra?

factu_total=total_dataset["payment_total"].sum()
clientes_total=total_dataset["customer_unique_id"].nunique()

gasto_por_cliente=factu_total/clientes_total

print(factu_total)
print(clientes_total)
print(f"Gasto medio por cliente: {gasto_por_cliente:.2f}")

# ¿Qué clientes realizan más pedidos?

clie=total_dataset.groupby("customer_unique_id").agg(
    pedidos=("order_id","nunique")
).sort_values(by="pedidos",ascending=False)
print("cliente que mas pedidos genera",clie)

# ¿Qué productos venden más unidades?
prod=total_dataset["product_id"].value_counts()

print("productos con ams unidades vendidas",prod)


# ¿Qué porcentaje de las operaciones terminan canceladas?

print(total_dataset["order_status"].value_counts())
canceladas1=total_dataset["order_status"]=="canceled"
canceladas_t=canceladas1.sum()
print(canceladas_t)
total_orders=total_dataset["order_status"].count()
pct_canceadas=canceladas_t/total_orders
print(f"{pct_canceadas:.2%} canceladas")


