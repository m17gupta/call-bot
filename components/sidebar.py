
import streamlit as st

def sidebar_menu():
    with st.sidebar:
        st.header("🧭 Navigation")
        st.page_link("pages/1_📦_Product_Listing.py", label="Product Listing")
        st.page_link("pages/2_🛒_Create_Order.py", label="Create Order")
        st.page_link("pages/3_📤_Upload_Excel.py", label="Upload Product Excel")
        st.page_link("pages/4_📑_Orders.py", label="Manage Orders")
