# BarMasters 🍻 - MVP 1

BarMasters é uma aplicação web que permite cadastrar, buscar, recomendar e avaliar bares. O projeto foi desenvolvido seguindo rigorosamente os princípios da **Clean Architecture** e **SOLID**, com backend em Flask e frontend independente.

---

## ⚡ Início Rápido (Automação via Scripts)

Para facilitar a execução no Linux ou Codespaces, criamos scripts que configuram tudo automaticamente.

### 1. Dê permissão de execução (Apenas na 1ª vez)
No terminal, na raiz do projeto, execute:

```bash
chmod +x run_server.sh run_client.sh run_tests.sh show_db.sh

2. Comandos de Execução
Ação	Comando	O que faz?
Rodar Servidor	./run_server.sh	Cria ambiente virtual, instala libs e sobe o backend (Porta 5000).
Rodar Site	./run_client.sh	Inicia o servidor do frontend (Porta 8000).
Rodar Testes	./run_tests.sh	Executa a bateria de testes unitários (Pytest).
Ver Banco	./show_db.sh	Exibe usuários, bares e avaliações formatados no terminal.
🛠️ Instalação Manual (Passo a Passo)

Caso prefira rodar manualmente ou esteja no Windows.
Backend (Servidor)

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

Inicie a API:
Bash

    python -m app.main

    O backend rodará em http://127.0.0.1:5000

Frontend (Cliente)

    Abra um novo terminal e vá para a pasta:
    Bash

cd client

Suba o servidor local:
Bash

    python3 -m http.server 8000

    Acesse no navegador: 👉 http://127.0.0.1:8000

📡 Endpoints da API

A comunicação entre Frontend e Backend é feita via JSON.
👤 Usuários

    POST /api/users → Registrar novo usuário.

    POST /api/users/login → Autenticar usuário (Retorna ID e Nome).

🍺 Bares

    POST /api/bars → Cadastrar novo bar (Exige owner_id).

    GET /api/bars/<id> → Obter detalhes de um bar específico.

    GET /api/bars/search?q=... → Buscar bares por nome ou endereço.

    GET /api/bars/newest → Listar os bares recém-cadastrados.

    GET /api/bars/random → Recomendação de bar aleatório.

    POST /api/bars/<id>/rate → Avaliar um bar (Nota 1-5 e comentário).

🧱 Arquitetura e Estrutura

O projeto segue a Clean Architecture, isolando regras de negócio de frameworks e bancos de dados.
Bash

server/
  ├── domain/       # Entidades Puras (User, Bar, Rating) - Sem dependências externas
  ├── use_cases/    # Regras de Negócio (Lógica da aplicação)
  ├── infra/        # Detalhes técnicos (Banco de Dados, Repositórios SQLite)
  ├── app/          # Framework Web (Rotas Flask, Configuração)
  ├── tests/        # Testes Unitários isolados
  └── db/           # Arquivo do banco SQLite (gerado automaticamente)

client/             # Frontend desacoplado (HTML/CSS/JS)

Diferenciais de Qualidade

    SOLID: Princípios aplicados (Ex: Inversão de Dependência nos repositórios).

    Testes: Cobertura de testes unitários para os casos de uso usando unittest.mock.

    PEP-8: Código formatado segundo as convenções Python.

    Automação: Scripts Shell para facilitar o setup e execução.

🗄️ Guia Manual do Banco de Dados

Se preferir acessar o banco manualmente sem o script ./show_db.sh:

    Acesse a pasta e abra o banco:
    Bash

cd server/db
sqlite3 bar_masters.db

Configure a visualização:
SQL

.headers on
.mode column

Exemplos de consultas:
SQL

SELECT * FROM users;
SELECT * FROM bars;
SELECT * FROM ratings WHERE score > 3;
.quit  -- Para sair