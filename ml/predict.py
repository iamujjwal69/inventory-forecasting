import pandas as pd
import numpy as np
from ml.feature_engineering import create_features

def generate_forecast_for_product(df, model, forecast_days=30):
    """
    df: historical daily sales (with columns sale_date, quantity)
    model: trained sklearn model
    Returns: list of predicted quantities for each future day.
    """
    # We'll do recursive prediction: for each future day, create features using
    # last available data and predicted values.
    df = df.copy()
    # Ensure we have all features
    df = create_features(df)
    feature_cols = [c for c in df.columns if c not in ["sale_date", "quantity"]]
    last_date = df["sale_date"].max()
    predictions = []
    # We'll use the last row's features as starting point
    last_row = df.iloc[-1].copy()
    # We need to maintain a list of recent values for lag features
    # We'll keep a rolling list of the last 30 actual or predicted values.
    # For simplicity, we'll just use the last actual values and append predictions.
    # More sophisticated: use the model to predict one day at a time, updating features.
    # We'll use a simple approach: for each day, we need to shift our data.
    # We'll create a DataFrame with future dates and fill features.
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days)
    # Prepare a list of dicts for future data
    future_rows = []
    # We'll use the last known values of lags and rolling stats.
    # For simplicity, we'll keep a copy of the last known series and update.
    series = list(df["quantity"].values)  # historical series
    for i, date in enumerate(future_dates):
        # Create a row with date features
        row = {
            "sale_date": date,
            "day_of_week": date.dayofweek,
            "month": date.month,
            "year": date.year,
            "day_of_year": date.dayofyear,
            "quarter": date.quarter,
            "weekend": 1 if date.dayofweek >= 5 else 0,
        }
        # Lags: need to get previous values from series (including predicted)
        # For lag_1: last value in series
        # For lag_7: value 7 days ago, etc.
        row["lag_1"] = series[-1] if len(series) >= 1 else 0
        row["lag_7"] = series[-7] if len(series) >= 7 else 0
        row["lag_14"] = series[-14] if len(series) >= 14 else 0
        row["lag_30"] = series[-30] if len(series) >= 30 else 0
        # Rolling mean of last 7 days (of actual or predicted)
        if len(series) >= 7:
            row["rolling_mean_7"] = np.mean(series[-7:])
            row["rolling_std_7"] = np.std(series[-7:])
        else:
            row["rolling_mean_7"] = 0
            row["rolling_std_7"] = 0
        # Predict using model
        X_future = pd.DataFrame([row])[feature_cols]
        pred = model.predict(X_future)[0]
        pred = max(0, int(round(pred)))
        predictions.append(pred)
        # Append predicted value to series for next iteration
        series.append(pred)
    return predictions
