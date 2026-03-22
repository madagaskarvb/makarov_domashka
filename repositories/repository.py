from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import AddProduct, ProductORM
from config.settings import settings
from typing import Optional

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(engine)

class ProductRepository:
    def __init__(self):
        self.db = SessionLocal

    def create(self, product_data: AddProduct) -> ProductORM:
        """Create a new product."""
        db_product = ProductORM(name=product_data.name, price=product_data.price, in_stock=product_data.in_stock)
        self.db.add(db_product)
        self.db.commit()
        return db_product

    def get_all(self, min_price: float = None, max_price: float = None, in_stock: bool = None) -> list[ProductORM]:
        """Get all products with optional filters."""
        query = self.db.query(ProductORM)
        if min_price is not None:
            query = query.filter(ProductORM.price >= min_price)
        if max_price is not None:
            query = query.filter(ProductORM.price <= max_price)
        if in_stock is not None:
            query = query.filter(ProductORM.in_stock == in_stock)
        return query.all()

    def get_by_id(self, product_id: int) -> Optional[ProductORM]:
        """Get a product by ID."""
        return self.db.query(ProductORM).filter(ProductORM.id == product_id)

    def replace(self, product_id: int, product_data: AddProduct) -> Optional[ProductORM]:
        """Replace a products fields."""
        db_product = self.get_by_id(product_id)
        if db_product:
            db_product.name = product_data.name
            db_product.price = product_data.price
            db_product.in_stock = product_data.in_stock
            self.db.commit()
        return db_product

    def delete(self, product_id: int) -> Optional[ProductORM]:
        """Delete a product by ID"""
        db_product = self.get_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return db_product
        return None