import pandas as pd
import numpy as np

def preprocess_sales_data(df):
    """
    Expects DataFrame with columns: sale_date (datetime), quantity (int)
    - Resample daily, fill missing with 0.
    - Remove outliers using IQR (cap at 3*IQR).
    """
    df = df.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df = df.set_index("sale_date").resample("D").sum().fillna(0)
    # Outlier capping
    q1 = df["quantity"].quantile(0.25)
    q3 = df["quantity"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 3 * iqr
    df["quantity"] = df["quantity"].clip(upper=upper)
    return df.reset_index()
