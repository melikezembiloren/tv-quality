from fastapi import FastAPI

from app.presentation.api.v1.routers.tv_router import router as tv_router

app = FastAPI(title="QualiTV API", version="0.1.0")

app.include_router(tv_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
