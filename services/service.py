from repositories.repository import ProductRepository
from repositories.models import AddProduct, ProductResponse
from typing import Optional

class ProductService():
    def __init__(self):
        self.repo = ProductRepository()


    def add_product(self, product: AddProduct) -> Optional[ProductResponse]:
        """Adding product"""
        prod = self.repo.create(product)
        if not prod:
            return None
        
        return ProductResponse(id=prod.id, name=prod.name, price=prod.price, in_stock=prod.in_stock)


    def get_product_by_id(self, id: int) -> Optional[ProductResponse]:
        """Getting product by id"""
        prod = self.repo.get_by_id(id)
        if not prod:
            return None
        
        return ProductResponse(id=prod.id, name=prod.name, price=prod.price, in_stock=prod.in_stock)
    

    def get_products(self, min_price: int=None, max_price: int=None, in_stock: int=None) -> Optional[list[ProductResponse]]:
        """Getting list of product with filter parameters"""
        prods = self.repo.get_all(min_price, max_price, in_stock)
        if not prods:
            return None
        
        return list(ProductResponse(id=prods.id, name=prods.name, price=prods.price, in_stock=prods.in_stock))
    

    def delete_product(self, product_id: int=None) -> Optional[ProductResponse]:
        """Deleting a product"""
        prod = self.repo.delete(product_id)
        if not prod:
            return None
        
        return ProductResponse(id=prod.id, name=prod.name, price=prod.price, in_stock=prod.in_stock)
    

    def replace_product(self, product_id: int=None, product_data=AddProduct) -> Optional[ProductResponse]:
        """Replacing a product"""
        prod = self.repo.replace(product_id, product_data)
        if not prod:
            return None
        
        return ProductResponse(id=prod.id, name=prod.name, price=prod.price, in_stock=prod.in_stock)

    