#!/usr/bin/env python3
"""
Script para iniciar o servidor FastAPI
"""
import uvicorn
import os
import sys

if __name__ == "__main__":
    # Adicionar o diretório atual ao path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Iniciar o servidor
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
