
import streamlit as st
import pandas as pd

st.title("🧾 Create Order")

# Load cart
cart = st.session_state.get("cart", [])

if not cart:
    st.warning("No items in cart. Please add products before creating an order.")
    st.stop()

df = pd.DataFrame(cart)
df["mrp"] = pd.to_numeric(df.get("mrp", 0), errors='coerce').fillna(0)
df["qty"] = pd.to_numeric(df.get("qty", 0), errors='coerce').fillna(0).astype(int)
df["subtotal"] = df["mrp"] * df["qty"]

st.dataframe(df[["sku", "description", "qty", "mrp", "subtotal"]], use_container_width=True)

discount_type = st.selectbox("Discount Type", ["Inclusive", "Exclusive", "Flat"])
discount_input = st.number_input("Discount Value (in % or ₹)", min_value=0.0)

total_pre_discount = df["subtotal"].sum()

if discount_type == "Flat":
    discount_amount = discount_input
elif discount_type == "Inclusive":
    discount_amount = (total_pre_discount * discount_input) / (100 + discount_input)
elif discount_type == "Exclusive":
    discount_amount = (total_pre_discount * discount_input) / 100
else:
    discount_amount = 0

total_after_discount = total_pre_discount - discount_amount

col1, col2 = st.columns(2)
with col1:
    st.metric("Total MRP", f"₹{total_pre_discount:,.2f}")
with col2:
    st.metric("Discounted Total", f"₹{total_after_discount:,.2f}")

if st.button("✅ Confirm Order"):
    st.success("🧾 Order confirmed and ready to be saved to DB (implement save next).")