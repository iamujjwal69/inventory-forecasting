from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, server_default=func.now())

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(Float, nullable=False)
    current_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="RESTRICT"))
    created_at = Column(DateTime, server_default=func.now())
    supplier = relationship("Supplier", back_populates="products")
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")
    transactions = relationship("InventoryTransaction", back_populates="product", cascade="all, delete-orphan")
    forecasts = relationship("Forecast", back_populates="product", cascade="all, delete-orphan")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    product = relationship("Product", back_populates="sales")
    __table_args__ = (Index("idx_product_date", "product_id", "sale_date"),)

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(Enum("in", "out", "adjustment"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, server_default=func.now())
    reference = Column(String(100))
    product = relationship("Product", back_populates="transactions")

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    forecast_date = Column(Date, nullable=False)
    predicted_demand = Column(Integer, nullable=False)
    model_name = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    product = relationship("Product", back_populates="forecasts")
    __table_args__ = (Index("idx_product_forecast", "product_id", "forecast_date"),)
