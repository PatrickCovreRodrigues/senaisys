#!/bin/bash

echo "🚀 Iniciando SENAI Backend API..."

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Arquivo requirements.txt não encontrado. Certifique-se de estar no diretório backend/"
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não está instalado. Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip não está instalado. Por favor, instale o pip."
    exit 1
fi

# Usar pip3 se disponível, senão usar pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "📦 Instalando dependências..."
$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências. Verifique o arquivo requirements.txt."
    exit 1
fi

echo "🗄️ Inicializando banco de dados..."
python3 -c "from database import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Banco de dados inicializado!')"

echo "📊 Populando banco com dados de exemplo..."
python3 populate_db.py

echo ""
echo "🌟 Backend iniciado com sucesso!"
echo ""
echo "📋 Endpoints disponíveis:"
echo "   • Documentação Swagger: http://127.0.0.1:8000/docs"
echo "   • Documentação ReDoc: http://127.0.0.1:8000/redoc"
echo "   • Health Check: http://127.0.0.1:8000/health"
echo ""
echo "🔧 Para iniciar o servidor:"
echo "   python3 run.py"
echo ""
echo "🧪 Para testar a API:"
echo "   python3 test_api.py"
echo "" 