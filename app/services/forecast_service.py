import pandas as pd
from sqlalchemy.orm import Session
from app.database.models import Product, Sale, Forecast
from app.config import settings
import joblib
import os
from datetime import datetime, timedelta
from ml.predict import generate_forecast_for_product

def get_forecast(product_id: int, db: Session, days: int = 30):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None, "Product not found"
    # Check if we have enough data
    sales = db.query(Sale).filter(Sale.product_id == product_id).order_by(Sale.sale_date).all()
    if len(sales) < 60:
        return None, "Insufficient historical sales data (need at least 60 days)"
    # Convert to DataFrame
    df = pd.DataFrame([(s.sale_date, s.quantity) for s in sales], columns=["sale_date", "quantity"])
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df = df.set_index("sale_date").resample("D").sum().fillna(0).reset_index()
    # Load model
    model_path = settings.MODEL_PATH
    if not os.path.exists(model_path):
        return None, "Model not trained yet. Please run training first."
    model = joblib.load(model_path)
    # Generate forecast
    forecast_dates = [(datetime.now() + timedelta(days=i)).date() for i in range(1, days+1)]
    predicted = generate_forecast_for_product(df, model, forecast_days=days)
    # Save forecasts to DB
    for i, date in enumerate(forecast_dates):
        f = Forecast(product_id=product_id,
                     forecast_date=date,
                     predicted_demand=predicted[i],
                     model_name="RandomForest"  # simplified
                     )
        db.add(f)
    db.commit()
    total_demand = sum(predicted)
    # Recommendation
    from app.services.recommendation_service import get_recommendation
    recom = get_recommendation(product.current_stock, total_demand, product.reorder_level)
    return {
        "product_id": product.id,
        "product_name": product.name,
        "forecast_period": f"{days}_days",
        "predicted_demand": total_demand,
        "daily_forecast": [{"date": d.isoformat(), "demand": p} for d, p in zip(forecast_dates, predicted)],
        "recommendation": recom,
        "model": "RandomForest"
    }, None
