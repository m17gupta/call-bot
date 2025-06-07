import pandas as pd

INVALID_STRINGS = ["-", "_"]

BASE_REQUIRED = ["sku", "description", "mrp", "gst"]
INTEGER_FIELDS = ["stock_88", "stock_90", "stock"]
FLOAT_FIELDS = ["mrp", "gst"]

BRAND_FIELDS = {
    "travismathews": [
        "sku", "description", "category", "season", "style_code", "color", "color_code", "size",
        "length", "gender", "line", "stock_90", "stock_88", "gst", "mrp"
    ],
    "ogios": [
        "sku", "description", "product_type", "category", "product_model",
        "stock_90", "gst", "mrp"
    ],
    "softgoods": [
        "sku", "description", "category", "season", "color", "style_id", "size",
        "gender", "sleeves", "stock_90", "stock_88", "gst", "mrp"
    ],
    "hardgoods": [
        "sku", "description", "mrp", "category", "gst", "stock_88",
        "product_type", "product_model", "orientation"
    ]
}

def validate_excel(df: pd.DataFrame, brand: str):
    errors = []
    corrected_df = df.copy()
    brand_key = brand.lower()

    required_fields = BRAND_FIELDS.get(brand_key, BASE_REQUIRED)

    # 1. Check if required columns are present
    for col in required_fields:
        if col not in corrected_df.columns:
            errors.append({
                "row": 0,
                "message": f"Missing required column: {col}"
            })

    # 2. Validate each row
    for idx, row in corrected_df.iterrows():
        for col in required_fields:
            value = row.get(col, None)

            if pd.isna(value) or (isinstance(value, str) and value.strip() in INVALID_STRINGS):
                corrected_df.at[idx, col] = "" if col not in INTEGER_FIELDS + FLOAT_FIELDS else 0
                errors.append({
                    "row": idx,
                    "message": f"Invalid or empty value in '{col}'"
                })

            if col in INTEGER_FIELDS:
                try:
                    corrected_df.at[idx, col] = int(float(value)) if value else 0
                except Exception:
                    corrected_df.at[idx, col] = 0
                    errors.append({
                        "row": idx,
                        "message": f"Invalid integer value in '{col}'"
                    })

            if col in FLOAT_FIELDS:
                try:
                    corrected_df.at[idx, col] = float(value) if value else 0.0
                except Exception:
                    corrected_df.at[idx, col] = 0.0
                    errors.append({
                        "row": idx,
                        "message": f"Invalid float value in '{col}'"
                    })

    is_valid = len(errors) == 0
    return is_valid, corrected_df, errors
