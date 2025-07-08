#!/bin/bash

echo "🎓 SENAI Frontend - Sistema de Gestão Acadêmica"
echo "==============================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para print colorido
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -d "backend" ] || [ ! -d "vue-project" ]; then
    print_error "Este script deve ser executado na raiz do projeto senaifront/"
    exit 1
fi

print_info "Iniciando configuração do projeto..."

# Configurar backend
echo ""
echo "🐍 Configurando Backend (FastAPI)..."
cd backend

# Verificar Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

# Determinar comando Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

print_info "Usando: $PYTHON_CMD"

# Verificar pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    print_error "pip não encontrado. Instale pip primeiro."
    exit 1
fi

# Determinar comando pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

print_info "Instalando dependências Python..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependências Python instaladas com sucesso"
else
    print_error "Falha ao instalar dependências Python"
    exit 1
fi

print_info "Populando banco de dados com dados de exemplo..."
$PYTHON_CMD populate_db.py

if [ $? -eq 0 ]; then
    print_status "Banco de dados populado com sucesso"
else
    print_warning "Aviso: Falha ao popular banco de dados (pode ser normal se já existir)"
fi

# Voltar para raiz
cd ..

# Configurar frontend
echo ""
echo "🖥️  Configurando Frontend (Vue.js)..."
cd vue-project

# Verificar Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js não encontrado. Instale Node.js 16+ primeiro."
    exit 1
fi

NODE_VERSION=$(node -v)
print_info "Usando Node.js: $NODE_VERSION"

# Verificar npm
if ! command -v npm &> /dev/null; then
    print_error "npm não encontrado. Instale npm primeiro."
    exit 1
fi

NPM_VERSION=$(npm -v)
print_info "Usando npm: $NPM_VERSION"

print_info "Instalando dependências Node.js..."
npm install

if [ $? -eq 0 ]; then
    print_status "Dependências Node.js instaladas com sucesso"
else
    print_error "Falha ao instalar dependências Node.js"
    exit 1
fi

# Voltar para raiz
cd ..

echo ""
print_status "✨ Configuração concluída com sucesso!"
echo ""
echo "🚀 Para iniciar o projeto:"
echo ""
echo "1️⃣  Backend (Terminal 1):"
echo "   cd backend"
echo "   python run.py"
echo ""
echo "2️⃣  Frontend (Terminal 2):"
echo "   cd vue-project"
echo "   npm run dev"
echo ""
echo "3️⃣  Acessar:"
echo "   🌐 Frontend: http://localhost:5173"
echo "   📚 API Docs: http://127.0.0.1:8000/docs"
echo "   ❤️  Health: http://127.0.0.1:8000/health"
echo ""
echo "📋 Dados de exemplo inclusos:"
echo "   • 4 Cursos (ADS, Ciência de Dados, etc.)"
echo "   • 3 Docentes com disponibilidades"
echo "   • 7 UCs vinculadas"
echo "   • 2 Calendários com eventos"
echo ""
print_status "Happy coding! 🎉" 