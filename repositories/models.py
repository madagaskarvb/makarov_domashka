from pydantic import BaseModel
from sqlalchemy import String, DECIMAL, Boolean, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

class Base(DeclarativeBase):
    pass

class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    price: Mapped[float] = mapped_column(DECIMAL)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)


    @validates("name")
    def check_name_length(self, key, value):
        if len(value) < 2 or len(value) > 80:
            raise ValueError("Name has to be 2-80 characters long")
        return value

    @validates("price")
    def check_non_negative(self, key, value):
        if value < 0:
            raise ValueError("Price can't be negative")
        return value
    

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class AddProduct(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ProductResponse(Product):
    pass