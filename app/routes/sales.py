from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Sale, Product, InventoryTransaction
from app.schemas.sales import SaleCreate, SaleResponse
from app.routes.products import get_current_user

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == sale_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.current_stock < sale_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    # Create sale record
    new_sale = Sale(product_id=sale_data.product_id,
                    sale_date=sale_data.sale_date,
                    quantity=sale_data.quantity,
                    unit_price=sale_data.unit_price)
    db.add(new_sale)
    # Update inventory
    product.current_stock -= sale_data.quantity
    # Create inventory transaction
    tx = InventoryTransaction(product_id=product.id,
                              transaction_type="out",
                              quantity=sale_data.quantity,
                              reference=f"Sale #{new_sale.id}")
    db.add(tx)
    db.commit()
    db.refresh(new_sale)
    return new_sale
