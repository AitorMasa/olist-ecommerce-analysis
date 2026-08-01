from pathlib import Path

ROOT =Path(__file__).resolve().parent

CLEAN = ROOT / "Clean" 
RAW = ROOT / "Raw"
ISSUES = ROOT / "Issues"
KPI = ROOT / "KPI"

for folder in [CLEAN,RAW,ISSUES,KPI]:
    folder.mkdir(parents=True, exist_ok=True)

CSV_FILES=["olist_customers_dataset.csv","olist_geolocation_dataset.csv","olist_order_items_dataset.csv",
           "olist_order_payments_dataset.csv","olist_order_reviews_dataset.csv","olist_orders_dataset.csv",
           "olist_products_dataset.csv","olist_sellers_dataset.csv","product_category_name_translation.csv"]





     
