"""
QIGA-Router FastAPI uygulaması.

Çalıştırmak için:
  uvicorn api.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs
ReDoc     : http://127.0.0.1:8000/redoc
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import cities, optimize

app = FastAPI(
    title="QIGA-Router API",
    description="Quantum-Inspired Genetic Algorithm for Travelling Salesman Problem",
    version="0.2.0",
)

# ALLOWED_ORIGINS env değişkeni virgülle ayrılmış origin listesi olarak verilir
# (örn. "https://qiga-router.vercel.app,http://localhost:3000"). Tanımlı değilse
# geliştirme ortamı için localhost'a izin verilir.
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(optimize.router, prefix="/api/v1", tags=["optimize"])
app.include_router(cities.router, prefix="/api/v1", tags=["cities"])


@app.get("/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok", "version": "0.2.0"}
