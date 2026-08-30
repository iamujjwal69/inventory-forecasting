import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
import joblib
import os
from app.database.connection import SessionLocal
from app.database.models import Sale
from ml.data_preprocessing import preprocess_sales_data
from ml.feature_engineering import create_features
from app.config import settings

def run_training(db_session=None):
    # If no session provided, create one
    if db_session is None:
        db = SessionLocal()
    else:
        db = db_session

    # Fetch all sales data
    sales = db.query(Sale).all()
    df = pd.DataFrame([(s.sale_date, s.quantity, s.product_id) for s in sales],
                      columns=["sale_date", "quantity", "product_id"])
    if df.empty:
        print("No sales data available for training.")
        return
    # For simplicity, we aggregate across all products (or we could do per product)
    # We'll just use the global sales series for demonstration.
    df = df.groupby("sale_date")["quantity"].sum().reset_index()
    df = preprocess_sales_data(df)
    df = create_features(df)
    # Drop NaN rows (due to shift)
    df = df.dropna().reset_index(drop=True)
    # Features and target
    feature_cols = [c for c in df.columns if c not in ["sale_date", "quantity"]]
    X = df[feature_cols]
    y = df["quantity"]
    # TimeSeriesSplit (chronological)
    tscv = TimeSeriesSplit(n_splits=3)
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    best_mae = float("inf")
    best_model = None
    best_name = None
    for name, model in models.items():
        mae_scores = []
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            mae = mean_absolute_error(y_test, preds)
            mae_scores.append(mae)
        avg_mae = np.mean(mae_scores)
        print(f"{name} average MAE: {avg_mae:.2f}")
        if avg_mae < best_mae:
            best_mae = avg_mae
            best_model = model
            best_name = name

    # Retrain on all data
    best_model.fit(X, y)
    # Save model
    os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
    joblib.dump(best_model, settings.MODEL_PATH)
    print(f"Best model ({best_name}) saved with MAE {best_mae:.2f}")
    if db_session is None:
        db.close()

if __name__ == '__main__':
    run_training()
