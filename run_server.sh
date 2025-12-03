#!/bin/bash

echo "🚀 Iniciando configuração do Backend..."

# 1. Entrar na pasta do servidor
cd server

# 2. Verificar se o ambiente virtual existe, se não, cria
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# 3. Ativar o ambiente virtual
source .venv/bin/activate

# 4. Instalar dependências (aponta para o arquivo dentro da pasta server)
echo "⬇️ Verificando dependências..."
pip install -r requirements.txt

# 5. Rodar o servidor (sem a pasta src, direto em app.main)
echo "🔥 Rodando o servidor Flask na porta 5000..."
python -m app.main