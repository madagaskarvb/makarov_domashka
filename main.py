from config.settings import settings
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.router import product_router

app = FastAPI(
    title="SigmaApp",
    version=settings.APP_VERSION,
    description="API для работы с товарами",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(product_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    Returnall info about API
    """
    return JSONResponse(
        content={
            "message": "Product Work API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "add_product": "POST /products/",
                "get_products": "GET /products/",
                "get_product": "GET /products/{id}",
                "update_product": "PUT /products/{id}",
                "delete_product": "DELETE /products/{id}"
            }
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check эндпоинт.
    Проверяет что API работает.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.APP_VERSION
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000
    )