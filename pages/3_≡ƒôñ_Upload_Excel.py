import streamlit as st
import pandas as pd
import importlib.util
from io import BytesIO
import os
import datetime
from utils.db import get_db
from validate_excel import validate_excel


st.set_page_config(layout="wide")
st.title("📤 Upload Product Excel by Brand")

brand = st.selectbox("Select Brand", ["hardgoods", "softgoods", "travismathews", "ogios"])
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

def load_validator(brand):
    try:
        base_dir = os.path.join(os.getcwd(), "validations")
        filepath = os.path.join(base_dir, f"{brand}.py")
        if not os.path.exists(filepath):
            return None, f"Validation file not found for {brand} → {filepath}"

        spec = importlib.util.spec_from_file_location(brand, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.validate_excel, None

    except Exception as e:
        return None, str(e)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🧾 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    valid, corrected_df, errors = validate_excel(df, brand=brand)

    if not validate_excel:
        st.error(f"❌ Failed to load validator for '{brand}': {errors}")
        st.stop()

    st.markdown("🔍 Running brand-specific validations...")
    valid, corrected_df, errors = validate_excel(df, brand=brand)

    for err in errors:
        if isinstance(err, dict):
            row = err.get('row', '?')
            message = err.get('message', 'Unknown error')
            st.markdown(f"- Row {row + 2 if isinstance(row, int) else row}: {message}")
        else:
            st.markdown(f"- {err}")


    st.subheader("✅ Validated / Corrected Data")
    st.dataframe(corrected_df, use_container_width=True)

    if st.button("📦 Save Valid Data to MongoDB"):
        db = get_db()
        col = db[brand]
        result = col.insert_many(corrected_df.to_dict("records"))
        # Log audit
        audit = db["upload_audit"]
        audit.insert_one({
            "brand": brand,
            "filename": uploaded_file.name,
            "row_count": len(corrected_df),
            "errors": len(errors),
            "status": "success" if valid else "partial",
            "timestamp": datetime.datetime.utcnow(),
            "notes": errors
        })
        st.success(f"✅ Inserted {len(result.inserted_ids)} records into '{brand}'")