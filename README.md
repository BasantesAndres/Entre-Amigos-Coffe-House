# 🍰 Dulce Gestión  
### Business Management and Product Demand Forecasting for a Small Coffee Shop

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Supabase](https://img.shields.io/badge/Backend-Supabase-green)
![ML](https://img.shields.io/badge/ML-MLPRegressor-purple)
![Status](https://img.shields.io/badge/Status-Functional-success)

> A full-stack academic project that combines **business operations management** with **product-level demand forecasting** in a single application.  
> Built for a small coffee shop / dessert shop scenario with modules for products, menu, orders, inventory, reports, and machine learning predictions.

---

## ✨ Project Overview

**Dulce Gestión** is a web application designed to help a small food business manage its daily operations while also supporting planning decisions through predictive analytics.

The system integrates:

- 🧾 product registration and stock control
- 📅 daily menu configuration
- 🛒 order registration and tracking
- 🚚 delivery status management
- 📊 reports and visualizations
- 💬 customer auto-response templates
- 🤖 demand forecasting with a neural network model

The app was developed with **Streamlit** as the user interface framework and **Supabase** for authentication and database persistence. In addition, a **Multi-Layer Perceptron (MLP)** regression model was integrated to estimate future product demand and suggest production quantities.

---

## 🚀 Why this project matters

Small businesses often manage products, sales, and inventory with fragmented tools or even manually. This causes:

- poor stock visibility
- weak sales traceability
- difficulty planning production
- overproduction or shortages
- lack of forecasting support

**Dulce Gestión** addresses this by connecting **operations + analytics + forecasting** in one platform.

---

## 🧱 Tech Stack

### Frontend
- **Streamlit**
- Custom CSS styling for dashboard polish
- Interactive data tables and charts

### Backend
- **Supabase Auth** for login/session management
- **Supabase PostgreSQL** as the operational database

### Data / Analytics
- **Pandas** for tabular processing
- **Plotly** for charts and visual reports

### Machine Learning
- **scikit-learn**
- **MLPRegressor**
- **NumPy**
- **joblib**

---

## 🏗️ Project Architecture

```bash
Entre-Amigos-Coffee-House/
│── .streamlit/
│   └── secrets.toml
│── components/
│   ├── cards.py
│   ├── header.py
│   └── sidebar.py
│── data/
│   ├── sales_history.csv
│   └── product_sales_history.csv
│── models/
│   ├── mlp_sales_model.pkl
│   └── product_mlp_model.pkl
│── pages/
│── utils/
│   ├── auth.py
│   ├── db.py
│   ├── generate_dataset.py
│   ├── generate_product_dataset.py
│   ├── ml_model.py
│   ├── product_ml_model.py
│   ├── state.py
│   └── styles.py
│── views/
│   ├── autorespuestas.py
│   ├── dashboard.py
│   ├── entregas.py
│   ├── inventario.py
│   ├── menu_diario.py
│   ├── pedidos.py
│   ├── predicciones.py
│   ├── productos.py
│   └── reportes.py
│── app.py
│── requirements.txt
```

> **Important note:** the application uses **`views/`** as the active page folder to avoid Streamlit’s automatic page navigation.  
> If `pages/` still exists in the repository, it is usually legacy or unused and can be removed if not needed.

---

## 📁 What each file/folder does

### `.streamlit/secrets.toml`
Stores private credentials such as:
- `SUPABASE_URL`
- `SUPABASE_KEY`

This file should **never** be exposed publicly with real credentials.

---

### `app.py`
Main entry point of the application.

Responsibilities:
- initializes Streamlit config
- initializes session state
- loads global styles
- shows login if user is not authenticated
- renders the custom sidebar
- routes the user to the correct view

---

### `components/`
Reusable UI components.

#### `components/sidebar.py`
Builds the custom navigation menu shown on the left side.

#### `components/header.py`
Renders the dashboard title and subtitle.

#### `components/cards.py`
Defines reusable stat cards for metrics like total products, low stock, daily sales, etc.

---

### `utils/`
Core logic helpers.

#### `utils/auth.py`
Handles authentication with Supabase:
- client creation
- session restoration
- login
- logout

#### `utils/state.py`
Initializes and protects `st.session_state` values such as:
- `authenticated`
- `page`
- `user_email`
- tokens

#### `utils/styles.py`
Contains the global CSS injected into Streamlit to improve the visual design.

#### `utils/db.py`
Main database layer.  
This file centralizes all CRUD and query operations for:
- products
- daily menu
- orders
- order items
- inventory movements
- dashboard stats
- report data

#### `utils/generate_dataset.py`
Creates a synthetic dataset for **daily total sales forecasting**.

#### `utils/ml_model.py`
Trains and evaluates the first forecasting model for **daily sales totals**.

#### `utils/generate_product_dataset.py`
Creates a synthetic dataset for **product-level demand prediction**.

#### `utils/product_ml_model.py`
Main ML module for forecasting units sold **per product**.

---

### `views/`
Contains each business module as an independent page.

#### `views/dashboard.py`
Main panel with:
- total products
- products on today’s menu
- orders today
- low stock alerts
- daily sales
- quick action buttons

#### `views/productos.py`
Full product CRUD:
- create product
- list products
- edit product
- delete product
- set active/inactive
- control stock and minimum stock

#### `views/menu_diario.py`
Allows selecting which products are available for the day.

#### `views/pedidos.py`
Registers customer orders, order items, payment method, and order status.

#### `views/inventario.py`
Controls stock movements:
- entrada
- salida
- ajuste

#### `views/entregas.py`
Manages order delivery status:
- pending
- in preparation
- on the way
- delivered
- canceled

#### `views/reportes.py`
Displays business analytics:
- sales by day
- total income
- average ticket
- top-selling products
- visual charts

#### `views/autorespuestas.py`
Generates automatic customer messages such as:
- order confirmation
- in preparation
- on the way
- delivered
- promotions

#### `views/predicciones.py`
ML dashboard for:
- synthetic dataset generation
- model training
- model evaluation
- product-level forecasting
- automatic production recommendations

---

### `data/`
Stores CSV datasets used for experimentation and forecasting.

- `sales_history.csv` → synthetic daily sales dataset
- `product_sales_history.csv` → synthetic per-product sales dataset

---

### `models/`
Stores trained ML artifacts serialized with `joblib`.

- `mlp_sales_model.pkl`
- `product_mlp_model.pkl`

---

## 🗄️ Database Architecture (Supabase)

The operational database is hosted in **Supabase PostgreSQL**.

Main tables used:

### `products`
Stores:
- product name
- category
- price
- stock
- minimum stock
- description
- status

### `daily_menu`
Stores which products are active in the menu for a given date.

### `orders`
Stores:
- customer data
- payment method
- notes
- status
- total order value

### `order_items`
Stores each product included in an order:
- product id
- quantity
- unit price
- subtotal

### `inventory_movements`
Stores stock changes with:
- product
- movement type
- quantity
- reason
- date

### Sales history
Sales history is reconstructed from the relationship between:
- `orders`
- `order_items`

This enables reporting and future forecasting.

---

## 🔐 Authentication Flow

The system uses **Supabase Auth**.

Flow:
1. the user enters email and password
2. Supabase validates credentials
3. access and refresh tokens are stored in Streamlit session state
4. the app restores the session if possible
5. logout clears the session and returns to login

This provides a simple but real authentication layer for the project.

---

## ⚙️ Functional Modules

### 1. 📦 Product Management
Allows complete CRUD for business products.

Features:
- add products
- update products
- delete products
- stock tracking
- minimum stock alerts
- active/inactive status

---

### 2. 📅 Daily Menu
Lets the business select what is available each day.

Why it matters:
- reflects real daily availability
- supports dynamic operations
- allows better short-term planning

---

### 3. 🛒 Orders
Registers customer purchases.

Features:
- customer information
- selected products
- quantities
- totals
- payment method
- notes
- order status

Orders also affect:
- inventory
- sales reports
- forecasting support

---

### 4. 🧾 Inventory Control
Tracks stock movements and supports operational discipline.

Movement types:
- **entrada**
- **salida**
- **ajuste**

When an order is created, stock is reduced automatically and a movement is logged.

---

### 5. 🚚 Deliveries
Provides status tracking for order fulfillment.

Useful statuses:
- pending
- in preparation
- on the way
- delivered
- canceled

This improves operational monitoring and customer communication.

---

### 6. 📊 Reports
The reporting module transforms raw operational data into business insight.

Implemented outputs:
- sales by day
- cumulative income
- average ticket
- top-selling products
- sales history table
- interactive charts

---

### 7. 💬 Auto Responses
Generates quick customer messages to improve communication.

Examples:
- “Your order has been received.”
- “Your order is in preparation.”
- “Your order is on the way.”
- “Your order has been delivered.”

---

## 🤖 Neural Network Module

One of the strongest parts of the project is the forecasting system.

### Goal
Estimate future demand to answer questions such as:
- how many chicken sandwiches will be sold tomorrow?
- how many brownies may be sold over the next 7 days?
- how many units should be prepared?

---

## 🧠 Why we used an MLP

We selected a **Multi-Layer Perceptron (MLP)** because:

- it is a neural network model suitable for **supervised regression**
- it is easier to integrate than a heavier recurrent model
- it works well with engineered lag-based temporal features
- it fits the academic scope of the project
- it is lightweight enough to run in a Streamlit app

This allowed us to include a real neural-network-based forecasting pipeline without overcomplicating deployment.

---

## 🧪 ML Problem Formulation

The forecasting task was defined as:

- **Learning type:** supervised learning
- **Problem type:** regression
- **Target variable:** `units_sold`

The model learns from examples where the inputs are known and the expected output (units sold) is also known.

---

## 📚 Synthetic Dataset for Forecasting

A synthetic dataset was generated covering **90 days** for **10 products** divided into two categories:

### Sandwiches
- chicken sandwich
- mixed sandwich
- ham sandwich
- tuna sandwich
- vegetarian sandwich

### Desserts
- cheesecake
- brownie
- chocolate tart
- tres leches
- filled cookie

Each row includes:

- `date`
- `product_name`
- `category`
- `day_of_week`
- `is_weekend`
- `promo`
- `price`
- `units_sold`

To provide recent historical memory to the network, we created:

- `lag_1`
- `lag_2`
- `lag_3`
- `rolling_mean_3`

These features simulate short-term temporal behavior.

---

## 🧠 Neural Network Architecture

The model was implemented with `MLPRegressor`.

Architecture:

```text
input → 64 → 32 → 1
```

### Configuration
- **hidden layers:** 64 and 32 neurons
- **activation:** ReLU
- **optimizer:** Adam
- **maximum iterations:** 1200
- **task:** regression
- **output:** predicted units sold

### Interpretation
- the **input layer** receives temporal and product-related features
- the **hidden layers** learn non-linear relationships
- the **output layer** predicts the expected number of units sold

---

## 🧮 Input Features Used by the Model

The product-level model uses:

- `day_of_week`
- `is_weekend`
- `promo`
- `price`
- `category_code`
- `product_code`
- `lag_1`
- `lag_2`
- `lag_3`
- `rolling_mean_3`

These features combine:
- business information
- temporal information
- recent demand memory

---

## 📏 Evaluation Metrics

The model is evaluated with:

### MAE
**Mean Absolute Error**

Measures the average absolute difference between the predicted value and the real value.

### RMSE
**Root Mean Squared Error**

Penalizes large prediction errors more strongly.

These metrics help quantify how well the model approximates future demand.

---

## 🔮 Forecasting Capabilities

The ML module can generate:

- next-day forecast for a selected product
- multi-day forecast for the next *x* days
- predictions for all products
- automatic production recommendations

This means the system can support operational decisions such as:
- what to prepare tomorrow
- which products to prioritize
- how much demand is expected during the next week

---

## 🧠 Recommendation Layer

On top of raw predictions, the system also generates operational recommendations.

Examples:
- classify demand as **High / Medium / Low**
- suggest how many units to prepare tomorrow
- indicate which products should be prioritized

This transforms the model from a purely academic forecasting task into a business support tool.

---

## 🧭 Application Flow

```text
User login
   ↓
Dashboard
   ↓
Products / Daily Menu / Orders / Inventory / Reports
   ↓
Sales history generation
   ↓
Forecasting module
   ↓
Predictions + production recommendations
```

---

## ✅ What was achieved

This project successfully delivered:

- a polished Streamlit dashboard
- real authentication with Supabase
- operational modules for a small food business
- persistent storage in PostgreSQL
- sales visualization and reporting
- a complete neural-network-based forecasting module
- product-level demand prediction
- production recommendation support

---

## 🎯 Why this project is valuable

This project is not just a CRUD demo.

It combines:

- **software engineering**
- **database integration**
- **UI/UX design**
- **business logic**
- **machine learning**
- **decision support**

In other words, it turns a small-shop scenario into a complete digital management and forecasting solution.

---

## 🔭 Future Work

Potential improvements include:

- using **real sales data** instead of synthetic data
- comparing **MLP vs LSTM**
- linking forecasts directly with inventory alerts
- deploying the application online
- isolating records by authenticated user
- adding CSV/PDF export
- integrating more advanced forecasting features

---

## 🛠️ Installation

```bash
git clone https://github.com/BasantesAndres/Entre-Amigos-Coffee-House.git
cd Entre-Amigos-Coffee-House
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create:

```bash
.streamlit/secrets.toml
```

With:

```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
```

---

## ▶️ Run the app

```bash
streamlit run app.py
```

---

## 📌 Recommended usage order

1. login
2. create products
3. configure daily menu
4. register orders
5. check inventory updates
6. explore reports
7. generate synthetic dataset
8. train forecasting model
9. inspect predictions and recommendations

---

## 📸 Suggested screenshots for presentation

If you want to showcase the project, the best screenshots are:

- dashboard overview
- products CRUD table
- reports chart
- forecasting chart
- recommendation table

---

## 👨‍💻 Author

**Andres Basantes**  
Yachay Tech University  
School of Mathematical and Computational Sciences

---

## 📄 License / Academic Use

This repository was developed for academic purposes as part of a university project involving software engineering, business systems, and neural networks.

---

## 🌟 Final Pitch

**Dulce Gestión** is a complete academic prototype that demonstrates how a modern web application can unify business operations and neural-network-based forecasting in a practical scenario. It goes beyond data registration by helping a small business understand its activity, monitor sales, control inventory, and anticipate demand.

If you want a project that combines **real application development** with **machine learning value**, this is it.
