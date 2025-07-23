from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cameras, mensagens, totens, usuarios

app = FastAPI(title="bairro Inteligente", description="Swagger e Redocs Bairro inteligente")

app.include_router(usuarios.router)
app.include_router(usuarios.protected_router)
app.include_router(cameras.protected_router)
app.include_router(totens.protected_router)
app.include_router(mensagens.protected_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)