# System Architecture and Operational Overview

This document provides an in-depth look at how the Inventory Forecasting System operates, the decision-making strategies it employs, how data is managed, and the reasoning behind the chosen technology stack.

## 1. How the System Works

The Inventory Forecasting System is a full-stack application designed to help businesses manage their product inventory proactively rather than reactively. 

### Core Workflow:
1. **Data Collection:** The system tracks real-time inventory levels (`current_stock`) and historical `Sale` transactions for each product.
2. **Machine Learning Pipeline:** A background task periodically trains a machine learning model on historical sales data to recognize patterns and trends.
3. **Forecasting & Prediction:** When a user requests a forecast (e.g., viewing a product on the Dashboard or Forecast page), the system uses the trained ML model to predict the daily demand for the next 30 days.
4. **Recommendation Generation:** The system compares the predicted 30-day demand against the currently available stock to generate actionable recommendations (e.g., how many units to reorder and the urgency status).

## 2. Decision-Making Strategies

The system does not just provide raw predictions; it applies business logic to generate concrete recommendations.

### Recommendation Logic (`recommendation_service.py`)
The system calculates a `safety_stock` (by default, 10% of the predicted demand) to buffer against unexpected spikes. It then calculates the `recommended_order` by subtracting the current stock from the sum of predicted demand and safety stock.

The urgency status is categorized as follows:
* **`OUT_OF_STOCK`**: Triggered immediately when `current_stock` is exactly 0.
* **`REORDER_REQUIRED`**: Triggered when the stock falls below the product's predefined minimum threshold (`reorder_level`).
* **`LOW_STOCK`**: Triggered when the current stock is lower than the AI-predicted demand for the next 30 days, indicating a high risk of stockouts.
* **`IN_STOCK`**: Triggered when the current stock comfortably meets the predicted demand.
* **`OVERSTOCKED`**: Triggered when the current stock exceeds 150% of the predicted demand, indicating capital is unnecessarily tied up in inventory.

## 3. Database and Data Sources

The system relies on a relational database to maintain data integrity.

* **Database Engine:** SQLite (`inventory.db`)
* **Data Sources:** 
  * **Products:** Manually added via the `/api/products` endpoints or initialized via mock data scripts.
  * **Sales History:** Generated every time a sale is made via the `/api/sales` endpoint. This endpoint automatically deducts the `current_stock` of the product and logs an `InventoryTransaction`.
* **Flow of Data into the Model:** The machine learning model strictly queries the `Sale` table, aggregating daily quantities sold per product to learn the demand curve. 

## 4. Technology Stack & Rationale

### Backend: FastAPI (Python)
* **Why:** Python is the industry standard for Data Science and Machine Learning. Using FastAPI allows us to serve the REST API and run the ML models within the same ecosystem effortlessly. FastAPI is also exceptionally fast, supports asynchronous programming, and automatically generates interactive API documentation.

### Database: SQLite & SQLAlchemy (ORM)
* **Why:** SQLite is a serverless, self-contained database that is perfect for MVPs and lightweight applications. By using SQLAlchemy as an Object Relational Mapper (ORM), the system is entirely database-agnostic. If the application needs to scale in the future, it can be migrated to PostgreSQL or MySQL simply by changing the connection string, without rewriting any SQL queries.

### Machine Learning: Scikit-Learn & Pandas
* **Why:** The system uses a `RandomForestRegressor` from `scikit-learn`. Random Forests are highly robust, handle non-linear relationships well, and require minimal hyperparameter tuning compared to deep learning models. `pandas` is used to resample and aggregate the raw sales data into a daily time-series format suitable for training.

### Frontend: Vanilla HTML, CSS, JavaScript & Chart.js
* **Why:** To keep the system lightweight and easily deployable without complex build pipelines (like Webpack or Node.js required by React/Angular). Vanilla JS fetches data asynchronously from the FastAPI backend, and `Chart.js` provides highly interactive and responsive data visualizations for the demand forecasts.
