from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Inicialização da aplicação
app = FastAPI(
    title="Classificador Inteligente de Emails API",
    description="API REST para classificação automática de emails usando IA",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configuração CORS - Ambientes permitidos
ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    # Adicione aqui o domínio de produção do frontend
    # "https://seu-frontend.vercel.app",
    # "https://seu-frontend.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=ALLOWED_ORIGINS,
    allow_origins=["https://email-classifier-frontend-i2kl.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Registrar rotas com prefixo /api
app.include_router(router, prefix="/api/v1", tags=["classificacao"])

# Health check na raiz
@app.get("/", tags=["sistema"])
async def root():
    """
    Endpoint raiz - Verifica se a API está online
    """
    return {
        "message": "Classificador Inteligente de Emails API",
        "status": "online",
        "version": "2.0.0",
        "docs": "/api/docs"
    }

@app.get("/health", tags=["sistema"])
async def health_check():
    """
    Health check detalhado
    """
    return {
        "status": "healthy",
        "service": "email-classifier-api",
        "version": "2.0.0"
    }

# Event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("API Classificador de Emails iniciada")
    logger.info("Documentação disponível em: /api/docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API Classificador de Emails encerrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )