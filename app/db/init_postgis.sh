#!/bin/bash
set -e

# Aguardando o banco de dados iniciar
sleep 10

# Executando comandos SQL
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
    CREATE EXTENSION IF NOT EXISTS postgis_topology;
    -- Adicione outros comandos SQL que desejar aqui
EOSQL
