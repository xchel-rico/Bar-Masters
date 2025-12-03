#!/bin/bash

echo "🧪 Preparando ambiente de testes..."

# 1. Entrar na pasta do servidor (onde estão os testes e o requirements.txt)
cd server

# 2. Verificar se o ambiente virtual existe; se não, cria
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# 3. Ativar o ambiente virtual
source .venv/bin/activate

# 4. Garantir que as dependências estão instaladas
echo "⬇️ Verificando dependências..."
pip install -r requirements.txt

# 5. Executar o Pytest
echo "🚀 Executando testes..."
echo "---------------------------------------------------"
python -m pytest
echo "---------------------------------------------------"