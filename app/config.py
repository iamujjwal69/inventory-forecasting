import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    # Use SQLite for a zero-friction setup
    DATABASE_URL = "sqlite:///./inventory.db"

    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    MODEL_PATH = os.getenv("MODEL_PATH", "ml/saved_models/demand_forecasting_model.pkl")

settings = Settings()
