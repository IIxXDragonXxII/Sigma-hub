#!/usr/bin/env bash

echo "Iniciando SIGMA HUB..."

# Verifica se a venv existe
if [ ! -d "venv" ]; then
    echo
    echo "[ERRO] A pasta 'venv' nao foi encontrada."
    echo "Execute primeiro o arquivo: ./instalar_bibliotecas.sh"
    echo
    read -rp "Pressione ENTER para sair..."
    exit 1
fi

# Ativa a venv
# shellcheck disable=SC1091
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo
    echo "[ERRO] Falha ao ativar o ambiente virtual."
    echo
    read -rp "Pressione ENTER para sair..."
    exit 1
fi

# Executa o programa
python3 main.py
if [ $? -ne 0 ]; then
    echo
    echo "[ERRO] O programa foi encerrado com erro."
    echo
    read -rp "Pressione ENTER para sair..."
    exit 1
fi

# Se chegou aqui, terminou normalmente
echo
echo "Programa finalizado. Pressione ENTER para fechar."
read -rp ""