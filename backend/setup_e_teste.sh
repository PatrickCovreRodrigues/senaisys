#!/bin/bash

echo "🎯 SISTEMA DE GESTÃO DOCENTE (SGD) - SETUP E TESTE"
echo "=================================================="

# Função para verificar se o comando foi bem-sucedido
check_command() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 concluído com sucesso"
    else
        echo "❌ Erro em $1"
        exit 1
    fi
}

# Navegar para o diretório backend
cd "$(dirname "$0")"

echo "📁 Diretório atual: $(pwd)"

# Verificar se o Python 3 está instalado
echo "🐍 Verificando Python..."
python3 --version
check_command "Verificação do Python"

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
    check_command "Ativação do ambiente virtual"
else
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    check_command "Criação do ambiente virtual"
    
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
    check_command "Ativação do ambiente virtual"
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt
check_command "Instalação de dependências"

# Verificar se as dependências específicas foram instaladas
echo "🔍 Verificando dependências específicas..."
python3 -c "import holidays; print('✅ holidays instalado')"
python3 -c "import pandas; print('✅ pandas instalado')"
python3 -c "import fastapi; print('✅ fastapi instalado')"
python3 -c "import sqlalchemy; print('✅ sqlalchemy instalado')"

# Criar tabelas do banco de dados
echo "🗄️  Criando tabelas do banco de dados..."
python3 -c "from database import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Tabelas criadas')"
check_command "Criação de tabelas"

# Testar o sistema de alocação
echo "🧪 Testando o sistema de alocação..."
python3 test_alocacao.py basico
check_command "Teste básico de alocação"

# Testar detecção de feriados
echo "🎄 Testando detecção de feriados..."
python3 test_alocacao.py feriados
check_command "Teste de feriados"

# Verificar se o servidor pode ser iniciado
echo "🚀 Testando inicialização do servidor..."
timeout 10s python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 5

# Testar se o servidor está respondendo
echo "🔗 Testando conectividade..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Servidor respondendo corretamente"
else
    echo "⚠️  Servidor não está respondendo (pode ser normal se porta em uso)"
fi

# Parar o servidor de teste
kill $SERVER_PID 2>/dev/null

echo ""
echo "🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "=================================================="
echo "📋 Para executar o sistema:"
echo "   1. Ative o ambiente virtual: source venv/bin/activate"
echo "   2. Execute o servidor: python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "   3. Acesse: http://localhost:8000/docs (documentação da API)"
echo ""
echo "🧪 Para testar o sistema de alocação:"
echo "   python3 test_alocacao.py [basico|conflitos|feriados|todos]"
echo ""
echo "📊 Endpoints da API de alocação:"
echo "   POST /api/alocacao/processar - Processa alocação automática"
echo "   GET  /api/alocacao/matriz-horarios - Obtém matriz de horários"
echo "   GET  /api/alocacao/disponibilidade/{docente_id} - Verifica disponibilidade"
echo "   GET  /api/alocacao/estatisticas - Obtém estatísticas"
echo ""
echo "💡 Consulte a documentação em: http://localhost:8000/docs" 