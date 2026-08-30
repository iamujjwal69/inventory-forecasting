# 🚀 AI-Based Inventory Demand Forecasting System

**Live Demo:** [https://inventory-forecasting-rd59.onrender.com/dashboard.html](https://inventory-forecasting-rd59.onrender.com/dashboard.html)

An end-to-end production-ready inventory management and demand forecasting system. This platform leverages Machine Learning (Random Forest) to analyze historical sales data, predict future inventory demand, and automatically recommend precise safety stock levels to prevent overstocking or stockouts.

## ✨ Key Features
- **🧠 AI Forecasting Engine**: Automated feature engineering (lags, rolling means, time-based features) and recursive multi-step forecasting for predicting the next 30 days of demand.
- **🛡️ Secure RESTful API**: Built with FastAPI, utilizing JWT token-based authentication and Bcrypt password hashing.
- **📊 Interactive Dashboard**: A frontend client utilizing Chart.js to visualize AI demand curves and real-time stock alerts.
- **🤖 Smart Recommendations**: Calculates safety stock dynamically based on AI predictions and flags items as `OUT_OF_STOCK`, `REORDER_REQUIRED`, `LOW_STOCK`, `IN_STOCK`, or `OVERSTOCKED`.
- **🗃️ Persistent Audit Trail**: Automatically logs an `InventoryTransaction` for every sale to maintain a perfect historical record.   

## 🛠️ Technology Stack
- **Backend Framework**: FastAPI (Python)
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Database Engine**: SQLite & SQLAlchemy (ORM)
- **Security**: JWT (Jose), Bcrypt
- **Frontend**: HTML5, Vanilla JS, Chart.js

## 📁 Architecture Overview
```text
inventory-forecasting/
├── app/                  # FastAPI Application Core
│   ├── routes/           # REST API Endpoints (Auth, Products, Sales, Forecast)
│   ├── services/         # Business Logic & ML Inference
│   ├── database/         # SQLite Connection & SQLAlchemy Models
│   └── schemas/          # Pydantic Validation Models
├── ml/                   # Machine Learning Pipeline
│   ├── feature_engineering.py  # Time-series transformations
│   ├── train.py                # Model training & evaluation 
│   └── saved_models/           # Serialized joblib models
├── frontend/             # Static UI Client
└── data/                 # Sample Data Generators
```

## 🚀 Quickstart Guide

### 1. Installation
Clone the repository and install the dependencies:
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Database Initialization & ML Training
To run the system, you first need to seed the database with sample historical data and train the AI model.

```bash
# 1. Generate 6-months of historical sales data and populate the database
python data/sample_data_generator.py

# 2. Run the ML pipeline to train and save the Random Forest model
python ml/train.py
```

### 3. Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The system will now be live at `http://localhost:8000`

### 4. Exploring the Platform
- **Frontend Dashboard**: Open your browser and navigate to `http://localhost:8000`. **Note:** You must first register a new account and log in before you can access the dashboard features!
- **Interactive API Docs**: Navigate to `http://localhost:8000/docs` to test endpoints directly via Swagger UI.

## 🧪 Running Tests
The project includes automated integration tests for the API layer and ML components.
```bash
pytest tests/
```

## 👤 Default User Account
If you used the sample data generator, the following admin account is available for testing:
- **Email**: `admin@example.com`
- **Password**: `admin123`
