from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://deepak:DeepakDBPass@callcluseter.bxdtpni.mongodb.net/")  # Update if hosted elsewhere
db = client["callaway_ai"]
orders_collection = db["orders"]

def get_next_order_id():
    latest_order = orders_collection.find_one(sort=[("id", -1)])
    return (latest_order["id"] + 1) if latest_order else 1000

def save_order(order_items, salesrep_id, retailer_id, manager_id, brand_id, discount_type):
    order_id = get_next_order_id()
    now = datetime.now()

    order_items_with_calcs = []
    total_val_pre_discount = 0
    total_discount_amt = 0

    for item in order_items:
        mrp = item["mrp"]
        qty = item.get("qty", 1)
        discount_percent = item.get("Discount", 0)

        pre_discount_amt = mrp * qty
        discount_amt = (pre_discount_amt * discount_percent / 100)
        final_amt = pre_discount_amt - discount_amt

        total_val_pre_discount += pre_discount_amt
        total_discount_amt += discount_amt

        order_items_with_calcs.append({
            "sku": item["sku"],
            "description": item["description"],
            "mrp": mrp,
            "qty": qty,
            "Discount": discount_percent,
            "Amount": final_amt,
            "LessDiscountAmount": discount_amt,
            "stock_88": item.get("stock_88", 0),
            "stock_90": item.get("stock_90", 0),
            "brand_id": item.get("brand_id", brand_id),
        })

    order_obj = {
        "id": order_id,
        "user_id": salesrep_id,
        "salesrep_id": salesrep_id,
        "retailer_id": retailer_id,
        "manager_id": manager_id,
        "brand_id": brand_id,
        "items": str(order_items_with_calcs),
        "discount_type": discount_type,
        "discount_percent": None,
        "discount_amount": round(total_discount_amt, 2),
        "total_val_pre_discount": round(total_val_pre_discount, 2),
        "total_value": round(total_val_pre_discount - total_discount_amt, 2),
        "status": "Pending",
        "order_date": now.isoformat(),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "note": [],
        "retailer_details": {},
        "manager_details": {},
        "salesRep_details": {},
        "manager_name": "",
        "retailer_address": "",
        "retailer_gstin": "",
        "retailer_name": "",
        "retailer_phone": "",
        "salesrep_name": "",
        "__v": 0
    }

    result = orders_collection.insert_one(order_obj)
    return {"status": "success", "order_id": order_id, "mongo_id": str(result.inserted_id)}
