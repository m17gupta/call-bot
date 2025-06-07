# 🧠 MasterVan: AI-Powered Product & Order Management System

**MasterVan** is a modular, scalable Streamlit-based system designed to manage branded product catalogs, automate order management workflows, and enable real-time user collaboration. Integrated with MongoDB and OpenAI GPT (when required), it streamlines product updates, validates Excel uploads, manages multi-role approvals, and supports four distinct brands.

---

## 🏷️ Brands Supported

* **Travis Mathew**
* **Callaway Hardgoods**
* **Callaway Softgoods**
* **Ogio**

Each brand maintains its own structure but shares a unified management interface.

---

## 👥 User Roles & Access Levels

### 1. **Admin**

* Master Admin access
* Create/Edit users
* View all orders and products
* Manage product uploads
* Backend order creation
* Global filtering and approvals

### 2. **Manager**

* Approve orders
* Create orders from backend
* Filter and edit products
* View and edit sales rep and retailer data

### 3. **Sales Representative**

* Create orders
* Filter products
* View brand-wise inventory and pricing

### 4. **Retailer** *(Coming Soon)*

* View selected products and submit order requests

---

## 🚀 Key Features

### 📦 Product Listing & Filtering

* Brand-wise product listing
* Support for category, product type, size, season, gender, and SKU filters
* Image handling and status tags (`has_image`, `image_done`)
* SKU Variants (handled via `variation_sku`)

### 📥 Excel Uploads

* Upload Excel sheets to update or add product data
* Per-brand field mapping (Travis, Callaway, Ogio)
* Inline preview before applying changes
* Smart duplicate detection based on `SKU`, `style_id`, or `description`

### ✅ Excel Validation Engine

* Mandatory field checks
* Format consistency per brand
* MRP, GST, and stock validation
* Error highlighting and inline fixing before commit

### 🛍️ Order Creation & Management

* Select products and input quantities
* Choose Discount Type:

  * `Inclusive`
  * `Exclusive`
  * `Flat`
* Auto calculate pre-discount and final totals
* Store complete breakdown in `orders` collection

### 🔐 Order Approval Flow

* Initiated by Sales Rep
* Reviewed and Approved by Manager
* Complete log stored in order `note` field

### 📊 Order Stats & Reporting

* Status breakdown: `Initiated`, `Pending`, `Approved`, `Rejected`
* Brand-wise and user-wise summary
* Logs include timestamps and action types

---

## 🧠 AI & Utility Modules

### GPT-Based Features *(on-demand)*

* Autogenerate product descriptions from brand/category
* Auto-suggest colors (e.g., roof → grey, polos → vibrant)
* Smart tag extraction (e.g., series, category)
* Bulk QA assistance for missing fields

### Developer Utilities

* **Live Watchdog Reload**

  * Automatically restart Streamlit app on file change
  * `python mastervan.py --watch`
* **Log Management**

  * Save logs in `/logs/` as `.json` and `.txt`
  * Per-feature logging for analysis
* **Test Mode**

  * Dry run for GPT/autofix before committing
  * `python mastervan.py --test`

---

## 📚 MongoDB Collections Structure

### 📦 Product Collections

* `hardgoods`
* `softgoods`
* `ogios`
* `travismathews`

Each collection includes fields like:

```json
{
  "sku": "string",
  "description": "string",
  "brand_id": 1,
  "category": "string",
  "mrp": 0,
  "gst": 0,
  "stock_88": 0,
  "stock_90": 0,
  "primary_image_url": "string",
  "variation_sku": "comma-separated",
  "has_image": 0
}
```

### 📑 Orders Collection

Stores complete structured order data:

* Discount logic (inclusive, exclusive, flat)
* User details for `salesrep`, `manager`, `retailer`
* Notes array for tracking activity
* Line item breakdown with quantity and stock check

### 👥 Users Collection

Stores metadata for all users, including:

* ID, Name, Role, Manager ID
* Phone numbers, Email, GSTIN, Status
* Role-based access controlled via Streamlit UI

---

## 📁 Suggested Folder Structure

```
project/
├── app.py                      # Streamlit main interface
├── mastervan.py                # CLI + watchdog runner
├── watcher.py                  # Live reload logic
├── material_extractor.py       # Material cleaning, profile check
├── requirements.txt
├── .env
├── logs/
│   └── order_logs.json
├── utils/
│   ├── validation.py
│   ├── log_manager.py
│   └── gpt_utils.py
└── uploads/
    └── excel_inputs.xlsx
```

---

## 🛠 To Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the app manually
streamlit run app.py

# Or use MasterVan CLI
python mastervan.py --watch --test --feature excel_uploader
```

---

## ✅ Future Enhancements

* Retailer Portal UI with product previews
* SKU image matching (using Vision AI)
* Sales dashboard with user ranking
* Downloadable Excel and PDF summaries
* Multilingual support (Hindi, English)
* API integration with ERP or logistics systems

---

Let me know if you'd like this README file saved, shared as markdown, or converted into a Streamlit starting structure!