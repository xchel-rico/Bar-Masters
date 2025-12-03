#!/bin/bash

echo "🌐 Iniciando Frontend..."

# 1. Entrar na pasta do cliente
cd client

# 2. Subir o servidor HTTP do Python
echo "🔥 Rodando site na porta 8000..."
python3 -m http.server 8000