# BarMasters 🍻 - MVP 1

BarMasters é uma aplicação que permite cadastrar, buscar, recomendar e avaliar bares. O projeto segue princípios de Clean Architecture, com backend em Flask e um frontend independente em HTML, CSS e JavaScript.

---

## ⚡ Início Rápido (Linux / Codespaces)

Para facilitar a execução, incluímos scripts de automação na raiz do projeto.

### 1. Dê permissão de execução (Apenas na 1ª vez)
Abra o terminal na pasta raiz e rode:

```bash
chmod +x run_server.sh run_client.sh

2. Rodar o Backend

Abra um terminal e execute:
Bash

./run_server.sh

Isso vai criar o ambiente virtual, instalar dependências e iniciar o servidor na porta 5000.
3. Rodar o Frontend

Abra outro terminal e execute:
Bash

./run_client.sh

Isso vai iniciar o site na porta 8000.
🛠️ Instalação Manual (Passo a Passo)

Caso prefira rodar os comandos manualmente ou esteja no Windows, siga as etapas abaixo.
Backend (Servidor)

    Pré-requisitos: Python 3.10+, pip e SQLite.

    Entre na pasta do servidor:
    Bash

cd server

Crie e ative o ambiente virtual:
Bash

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
# python -m venv .venv
# .venv\Scripts\activate

Instale as dependências:
Bash

pip install -r requirements.txt

Execute o programa:
Bash

    python -m app.main

    O servidor rodará em: http://127.0.0.1:5000

Frontend (Cliente)

    Abra um novo terminal e vá até a pasta:
    Bash

cd client

Inicie o servidor estático local:
Bash

    python3 -m http.server 8000

    Acesse no navegador: 👉 http://127.0.0.1:8000

📡 API – Endpoints principais
Autenticação

    POST /api/users → Registrar usuário

    POST /api/users/login → Fazer login

Bares

    POST /api/bars → Cadastrar bar

    GET /api/bars/<id> → Detalhes de um bar

    GET /api/bars/random → Recomendar bar aleatório

    GET /api/bars/search?q= → Buscar bares

    GET /api/bars/newest → Listar novos bares

    POST /api/bars/<id>/rate → Avaliar bar

Todas as respostas são em JSON.
🧱 Arquitetura (Clean Architecture)
Bash

server/
  app/         → Rotas e Configuração (Frameworks & Drivers)
  domain/      → Entidades Puras (Enterprise Business Rules)
  use_cases/   → Regras de Negócio da Aplicação
  infra/       → Repositórios e Banco de Dados (Interface Adapters)
client/
  *.html       → Páginas (Login, Busca, Cadastro, etc.)
  app.js       → Lógica do Frontend
  styles.css   → Estilização

📘 GUIA: Gerenciando o Banco de Dados (SQLite)

Comandos para visualizar os dados diretamente pelo terminal.
1. Acessar o Banco
Bash

cd server/db
sqlite3 bar_masters.db

2. Configurar Visualização

Ao entrar no sqlite>, digite:
SQL

.headers on
.mode column

3. Comandos Úteis
SQL

-- Ver usuários
SELECT * FROM users;

-- Ver bares
SELECT * FROM bars;

-- Ver avaliações
SELECT * FROM ratings;

-- Sair
.quit