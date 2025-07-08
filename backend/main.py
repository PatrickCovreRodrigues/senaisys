from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import cursos, docentes, ucs, calendario, alocacao

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SENAI Frontend Backend API",
    description="API para gerenciamento de cursos, docentes, UCs e calendários do SENAI",
    version="1.0.0"
)

# Configuração CORS para permitir requests do frontend Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(cursos.router, prefix="/api/cursos", tags=["cursos"])
app.include_router(docentes.router, prefix="/api/docentes", tags=["docentes"])
app.include_router(ucs.router, prefix="/api/ucs", tags=["ucs"])
app.include_router(calendario.router, prefix="/api/calendario", tags=["calendario"])
app.include_router(alocacao.router, prefix="/api", tags=["alocacao"])

@app.get("/")
async def root():
    return {"message": "SENAI Backend API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 