
import streamlit as st
from components.sidebar import sidebar_menu

st.set_page_config(layout="wide", page_title="MasterVan")

sidebar_menu()

st.title("📦 MasterVan - Product & Order Dashboard")
st.markdown("Use the sidebar to navigate.")
