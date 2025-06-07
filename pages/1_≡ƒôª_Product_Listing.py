import streamlit as st
import pandas as pd
from utils.db import get_collection

st.set_page_config(layout="wide")
st.title("📦 Product Listing")



brand = st.selectbox("Select Brand", ["travismathews", "hardgoods", "softgoods", "ogios"], index=0)

collection = get_collection(brand)
data = list(collection.find({}, {"_id": 0}))
#data = get_collection(brand)

if "cart" not in st.session_state:
    st.session_state.cart = []
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "table"

# Toggle between Table and Variation Group View
st.toggle("🔁 Switch to Variation Group View", key="view_mode_toggle")
st.session_state.view_mode = "group" if st.session_state.view_mode_toggle else "table"

if data:
    df = pd.DataFrame(data).fillna("")

    # Remove unnecessary fields
    hidden_cols = ["_id", "createdAt", "updatedAt", "__v", "has_image", "image_done", "gallery_images_url", "style_code Code","Image","primary_images_url","size_type","brand_id"]
    df = df.drop(columns=[col for col in hidden_cols if col in df.columns])

    # Compute stock fields
    df["stock_88"] = pd.to_numeric(df.get("stock_88", 0), errors='coerce').fillna(0).astype(int)
    df["stock_90"] = pd.to_numeric(df.get("stock_90", 0), errors='coerce').fillna(0).astype(int)
    df["total_stock"] = df["stock_88"] + df["stock_90"]
    df["qty"] = 0
    df["cart"] = False

    # Optional image
    if "primary_image_url" in df.columns:
        df["preview"] = df["primary_image_url"].apply(lambda x: f"https://yourcdn.com/images/{x}" if x else "https://via.placeholder.com/80")

    # Filters
    filter_cols = ["category", "gender", "season", "size", "style_code"]
    with st.expander("🔍 Filters"):
        for col in filter_cols:
            if col in df.columns:
                options = sorted(df[col].dropna().astype(str).unique().tolist())
                selected = st.multiselect(f"Filter by {col}", options, default=options)
                df = df[df[col].astype(str).isin(selected)]

    # Pagination
    rows_per_page = 200
    total_rows = len(df)
    page_number = st.number_input("Page", min_value=1, max_value=max((total_rows - 1) // rows_per_page + 1, 1), value=1, step=1)
    start_idx = (page_number - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    paginated_df = df.iloc[start_idx:end_idx]

    if st.session_state.view_mode == "table":
        edited_df = st.data_editor(
            paginated_df,
            use_container_width=True,
            key=f"editor_page_{page_number}",
            column_config={
                "preview": st.column_config.ImageColumn("Image", width="small"),
                "cart": st.column_config.CheckboxColumn("Add to Cart", default=False),
                "qty": st.column_config.NumberColumn("Qty", min_value=0, step=1)
            },
            disabled=["variation_sku", "primary_image_url"]
        )
        st.session_state.cart = edited_df[(edited_df["cart"] == True) & (edited_df["qty"] > 0)].to_dict("records")
        st.success(f"🛒 {len(st.session_state.cart)} item(s) added to cart")

    else:  # Group View
        st.markdown("### 🔁 Grouped Variations")
        if "variation_sku" in df.columns:
            for idx, row in paginated_df.iterrows():
                var_skus = [sku.strip() for sku in str(row.get("variation_sku", "")).split(",") if sku.strip()]
                group_df = df[df["sku"].isin(var_skus)]
                if not group_df.empty:
                    with st.expander(f"{row['description']} | Style: {row.get('style_code', '')}"):
                        group_df["qty"] = 0
                        group_df["cart"] = False
                        st.data_editor(
                            group_df,
                            use_container_width=True,
                            key=f"group_variation_{row.get('sku', idx)}",
                            column_config={
                                "cart": st.column_config.CheckboxColumn("Add to Cart", default=False),
                                "qty": st.column_config.NumberColumn("Qty", min_value=0, step=1)
                            },
                            disabled=["variation_sku", "primary_image_url"]
                        )
else:
    st.warning("No data found for this brand.")