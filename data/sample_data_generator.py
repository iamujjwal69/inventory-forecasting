import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from datetime import datetime, timedelta
from app.database.connection import SessionLocal, engine, Base
from app.database.models import Supplier, Product, Sale, InventoryTransaction

Base.metadata.create_all(bind=engine)

def generate_sample_data():
    db = SessionLocal()
    # Suppliers
    sup = Supplier(name="Acme Corp", email="acme@example.com")
    db.add(sup)
    db.commit()
    # Products
    products = []
    for i in range(1, 21):
        p = Product(name=f"Product {i}", category=random.choice(["Electronics","Clothing","Food"]),
                    price=round(random.uniform(10, 500), 2),
                    current_stock=random.randint(10, 100),
                    reorder_level=random.randint(5, 20),
                    supplier_id=sup.id)
        db.add(p)
        products.append(p)
    db.commit()
    # Sales for last 6 months
    start_date = datetime.now() - timedelta(days=180)
    for day in range(180):
        date = start_date + timedelta(days=day)
        for p in products:
            if random.random() < 0.3:  # some days no sales
                continue
            qty = random.randint(1, 10)
            sale = Sale(product_id=p.id, sale_date=date, quantity=qty, unit_price=p.price)
            db.add(sale)
            # Inventory transaction
            tx = InventoryTransaction(product_id=p.id, transaction_type="out",
                                      quantity=qty, reference="Sale", transaction_date=date)
            db.add(tx)
            p.current_stock -= qty
    db.commit()
    db.close()

if __name__ == "__main__":
    generate_sample_data()
