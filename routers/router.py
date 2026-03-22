from fastapi import APIRouter, HTTPException, status, Depends
from repositories.models import ProductResponse, AddProduct
from services.service import product_service

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.post(
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Added product"},
        400: {"description": "Failed to add product"},
    }
)
async def add_product(product: AddProduct):
    """
    Adds products

    Response codes:
    200 - successfully added product
    400 - attempt to add product failed
   
    """
    
    product_data = product_service.add_product(product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed request or invalid JSON",
        )
    
    return ProductResponse(**product_data)