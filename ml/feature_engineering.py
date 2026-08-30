import pandas as pd

def create_features(df):
    """
    Add date features, lags, and rolling statistics.
    Avoid leakage: use shift to ensure features are from past data.
    """
    df = df.copy()
    # Date features
    df["day_of_week"] = df["sale_date"].dt.dayofweek
    df["month"] = df["sale_date"].dt.month
    df["year"] = df["sale_date"].dt.year
    df["day_of_year"] = df["sale_date"].dt.dayofyear
    df["quarter"] = df["sale_date"].dt.quarter
    df["weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Lags
    for lag in [1, 7, 14, 30]:
        df[f"lag_{lag}"] = df["quantity"].shift(lag).fillna(0)

    # Rolling stats (7-day window)
    df["rolling_mean_7"] = df["quantity"].rolling(7, min_periods=1).mean().shift(1).fillna(0)
    df["rolling_std_7"] = df["quantity"].rolling(7, min_periods=1).std().shift(1).fillna(0)
    return df
