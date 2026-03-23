from fastapi import APIRouter, HTTPException, status, Query
from repositories.models import ProductResponse, AddProduct
from services.service import product_service

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Added product"},
        400: {"description": "Failed to add product"},
    }
)
async def add_product(product: AddProduct):
    """
    Adds products

    Response codes:
    201 - successfully added product
    400 - attempt to add product failed
   
    """
    
    product_data = product_service.add_product(product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed request or invalid JSON",
        )
    
    return product_data


@product_router.get(
    "/",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
        responses={
        200: {"description": "Retrieved products"},
        400: {"description": "Failed to retrieve products"},
    }
)
async def list_products(
    min_price: float = Query(None, description="Minimum price filter"),
    max_price: float = Query(None, description="Maximum price filter"),
    in_stock: bool = Query(None, description="Filter by stock status"),
):
    """
    Retrieve all products with optional filters.

    Response codes:
    200 - successfully retrieved products
    400 - failed to retrieve products
    """

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price",
        )

    products = product_service.get_products(min_price, max_price, in_stock)
    return products


@product_router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Found product"},
        404: {"description": "Product not found"},
    }
)
async def get_product(product_id: int):
    """
    Retrieve a product by its ID.
    """
    product = product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


@product_router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Product replaced successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "Product not found"},
    }
)
async def replace_product(product_id: int, product: AddProduct):
    """
    Fully replace an existing product. All fields are required.
    """
    replaced = product_service.replace_product(product_id, product)
    if replaced is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return replaced


@product_router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Product deleted successfully"},
        404: {"description": "Product not found"},
    }
)
async def delete_product(product_id: int):
    """
    Delete a product by its ID.
    """
    deleted = product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return deleted