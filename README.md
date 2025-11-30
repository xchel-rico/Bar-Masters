# BarMasters API – Primeira versão (sem front-end)

Esta é a primeira versão de teste da API do BarMasters, apenas com o backend em Python
(sem HTML, CSS ou JavaScript).

---

## 🚀 Como rodar o backend (server)

### 1. Pré-requisitos

- Python 3.10+ instalado  
- `pip` instalado  
- SQLite (normalmente já vem instalado no sistema)

### 2. Clonar o repositório

```bash
git clone https://github.com/xchel-rico/Bar-Masters.git
cd Bar-Masters/server
```

### 3. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Executar o programa

```bash
python -m src.app.main
```

Depois, abra o navegador e acesse: 
```bash
http://127.0.0.1:5000
```
(Ajuste a porta se o seu projeto usar outra.)

## 🖥️ Como rodar o frontend (client)

### 1. Vá até a pasta:

```bash
cd Bar-Masters/client
```

### 2. Abra o arquivo:

```bash
index.html
```

Dê um duplo clique ou abra no navegador.

### Opção 2: usar um servidor estático local

```bash
cd Bar-Masters/client
python -m http.server 8000
```

Abra:

```bash
http://127.0.0.1:8000
```

## 📡 API – Endpoints principais
### Usuários

- ```POST /api/users``` → Registrar usuário

### Bares

- ```POST /api/bars``` → Cadastrar bar

- ```GET /api/bars/random``` → Recomendar bar aleatório

- ```GET /api/bars/search?q=``` → Buscar bares

- ```GET /api/bars/newest``` → Listar novos bares

- ```POST /api/bars/<id>/rate``` → Avaliar bar

Todas as respostas são em JSON.

## 🧱 Arquitetura (Clean Architecture)

``` bash
server/
  app/         → rotas (controllers)
  domain/      → entidades
  use_cases/   → regras de negócio
  infra/       → repositórios + db
client/
  index.html
  styles.css
  app.js
  config.js
```

## ✔️ Status Atual

- Backend completo (Flask + SQLite)

- Frontend básico implementado (HTML/CSS/JS puros)

- Comunicação via fetch + JSON

- Estrutura separada entre frontend e backend