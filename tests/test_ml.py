import pandas as pd
from ml.data_preprocessing import preprocess_sales_data
from ml.feature_engineering import create_features

def test_preprocessing():
    df = pd.DataFrame({
        "sale_date": ["2023-01-01", "2023-01-03"],
        "quantity": [5, 10]
    })
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    processed = preprocess_sales_data(df)
    assert processed["sale_date"].nunique() == 3  # includes missing day 2023-01-02 with 0
    assert processed["quantity"].sum() == 15
