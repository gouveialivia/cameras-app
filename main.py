from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.rotas import router, protected_router

app = FastAPI(title="bairro Inteligente", description="Swagger e Redocs Bairro inteligente")

app.include_router(router)
app.include_router(protected_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)