import pandas as pd

# ¿Cómo ha evolucionado la facturación mes a mes?
def facturacion_evolucion (df):
    df = df.copy()
    df["order_purchase_timestamp"]=pd.to_datetime(df["order_purchase_timestamp"],format="mixed",errors="coerce",dayfirst="true")
    df["order_purchase_timestamp_month"]=df["order_purchase_timestamp"].dt.month
    df["order_purchase_timestamp_y_m"]=(df["order_purchase_timestamp"].dt.to_period("M"))
    resultado=df.groupby("order_purchase_timestamp_y_m").agg(
        facturacion=("payment_total","sum")
    ).sort_index()
    return resultado
    #print(facturacion_mensual)
    #print(df["order_purchase_timestamp"].max())
    #print(df[df["order_purchase_timestamp_y_m"] == "2018-09"])
    #mask=df["order_id"]=="54282e97f61c23b78330c15b154c867d"
    #print(df.loc[mask, ["order_id", "order_purchase_timestamp","payment_total","payment_installments"]])
    #mask = df["order_purchase_timestamp"].dt.year == 2016
    #print(df.loc[ mask, "order_purchase_timestamp"].sort_values())
    #print(print(df.loc[mask,"order_purchase_timestamp_y_m"].value_counts().sort_index()))
    #mask = (df["order_purchase_timestamp"].dt.year == 2018) & (df["order_purchase_timestamp"].dt.month==3)
    #print(df.loc[mask,["order_id", "order_purchase_timestamp","payment_total","payment_installments"]])


# ¿Qué productos generan más ingresos para la empresa?
def mejores_productos (df):
    resultado=(
    df.groupby("product_id").agg(
        price_total=("price","sum")
    ).sort_values(by="price_total",ascending=False)
    )
    return resultado

#  ¿Qué clientes generan más ingresos para la empresa?
def mejores_clientes (df):
    resultado=(
    df.groupby("customer_unique_id").agg(
        ingresos=("payment_total","sum")
    ).sort_values(by="ingresos",ascending=False))
    #print("cliente que mas ingresos genera",cli)
    #print(df["customer_id"].nunique())
    #print(df["customer_unique_id"].nunique())
    return resultado

# ¿Qué Facturación por estado la empresa?
def facturacion_por_estado (df):
    
    resultado=(df.groupby("customer_state").agg(
        price=("payment_total","sum")
    ).sort_values(by="price",ascending=False))
    #print("estado que mas facturacion genera:", estado)
    return resultado

# ¿Cuánto gasta de media un cliente en cada compra?

def ingreso_medio_por_cliente (df):
    
    factu_total=df["payment_total"].sum()
    clientes_total=df["customer_unique_id"].nunique()
    ingreso_medio_por_cliente=factu_total/clientes_total
    return ingreso_medio_por_cliente
    #print(factu_total)
    #print(clientes_total)
    #print(f"Gasto medio por cliente: {gasto_por_cliente:.2f}")

# ¿Qué clientes realizan más pedidos?
def clientes_mas_pedidos (df):
    
    resultado=(df.groupby("customer_unique_id").agg(
        pedidos=("order_id","nunique")
    ).sort_values(by="pedidos",ascending=False))
    #print("cliente que mas pedidos genera",resultado)
    return resultado

# ¿Qué productos venden más unidades?
def producto_mas_ventas (df):
    
    resultado=(df["product_id"].value_counts())
    #print("productos con ams unidades vendidas",prod)
    return resultado

# ¿Qué porcentaje de las operaciones terminan canceladas?
def operaciones_canceladas (df):
    df=df.copy()
    #print(df["order_status"].value_counts())
    canceladas1=df["order_status"]=="canceled"
    canceladas_t=canceladas1.sum()
    #print(canceladas_t)
    total_orders=df["order_status"].count()
    pct_canceadas=canceladas_t/total_orders
    #print(f"{pct_canceadas:.2%} canceladas")
    return pct_canceadas

# ¿Qué clientes cancelan más pedidos?
def clientes_cancelaciones (df):
    
    #print(df.columns)
    #print(df["order_status"].value_counts())
    df["canceled"]=df["order_status"]== "canceled"
    resultado=(df.groupby("customer_unique_id").agg(
        total= ("canceled","sum")
    ).sort_values(by="total",ascending=False))
    #print("clientes que mas cancelan",resultado)
    return resultado

#¿Qué porcentaje de la facturación total generan los 20 clientes más importantes?

def top_20_clientes (df):
    
    resultado=(df.groupby("customer_unique_id").agg(
        total=("payment_total","sum")
    ).sort_values(by="total",ascending=False).head(20))
    #print("df",resultado)
    return resultado


# ¿Qué porcentaje de la facturación total generan los 20 productos más importantes?
def top_20_facturacion (df):
    
    resultado=(df.groupby("product_id").agg(
        factu=("payment_total","sum")
    ).sort_values(by="factu",ascending=False).head(20))
    #print(resultado)
    return resultado


