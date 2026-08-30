from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, products, sales, forecast
from app.database.connection import engine, Base
import os

app = FastAPI(title="Inventory Forecasting System")

# Create tables (if not exist)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(forecast.router)

# Ensure frontend dir exists before mounting
os.makedirs("frontend", exist_ok=True)
# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
