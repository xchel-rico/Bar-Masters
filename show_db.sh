#!/bin/bash

DB_PATH="server/db/bar_masters.db"

echo "📊 Lendo Banco de Dados: $DB_PATH"

# Verifica se o arquivo existe
if [ ! -f "$DB_PATH" ]; then
    echo "❌ Erro: O arquivo do banco de dados não foi encontrado!"
    echo "   Certifique-se de ter rodado o servidor pelo menos uma vez."
    exit 1
fi

# Executa os comandos SQL automaticamente
sqlite3 -header -column "$DB_PATH" <<EOF
.print "\n========================================"
.print "👤  USUÁRIOS CADASTRADOS"
.print "========================================"
SELECT id, name, email, created_at FROM users;

.print "\n========================================"
.print "🍻  BARES CADASTRADOS"
.print "========================================"
SELECT id, name, address, owner_id FROM bars;

.print "\n========================================"
.print "⭐  AVALIAÇÕES"
.print "========================================"
SELECT id, bar_id, user_id, score, comment FROM ratings;
EOF