from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.forecast_service import get_forecast
from app.routes.products import get_current_user
from ml.train import run_training

router = APIRouter(prefix="/api/forecast", tags=["forecast"])

@router.get("/{product_id}")
def forecast_product(product_id: int, days: int = 30, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = get_forecast(product_id, db, days)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result

@router.post("/train")
def train_model(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can trigger training")
    background_tasks.add_task(run_training, db)
    return {"message": "Training started in background"}
