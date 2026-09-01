#!/usr/bin/env bash

echo "========================================================"
echo " INSTALADOR DE BIBLIOTECAS - SIGMA HUB"
echo "========================================================"
echo

# Verifica Python
echo "[1/5] Verificando Python..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERRO] Python nao encontrado. Instale o Python 3 e tente novamente."
    read -rp "Pressione ENTER para sair..."
    exit 1
fi
python3 --version
echo

# Verifica pip
echo "[2/5] Verificando pip..."
if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "[ERRO] pip nao encontrado. Tente reinstalar o Python."
    read -rp "Pressione ENTER para sair..."
    exit 1
fi
echo

# Cria venv se não existir
echo "[3/5] Criando ambiente virtual (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar a venv."
        read -rp "Pressione ENTER para sair..."
        exit 1
    fi
    echo "Ambiente virtual criado."
else
    echo "Ambiente virtual ja existe."
fi
echo

# Ativa venv e instala bibliotecas
echo "[4/5] Instalando bibliotecas..."
# shellcheck disable=SC1091
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao ativar a venv."
    read -rp "Pressione ENTER para sair..."
    exit 1
fi

echo "Atualizando pip..."
python3 -m pip install --upgrade pip

echo "Instalando dependencias..."
pip install customtkinter Pillow opencv-python pygame flask

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha na instalacao de alguma biblioteca."
    read -rp "Pressione ENTER para sair..."
    exit 1
fi

# Gera requirements.txt
echo "[5/5] Gerando requirements.txt..."
pip freeze > requirements.txt
echo "requirements.txt atualizado."

echo
echo "========================================================"
echo " INSTALACAO CONCLUIDA COM SUCESSO!"
echo " Todas as bibliotecas estao prontas."
echo " Agora execute o arquivo: ./iniciar.sh"
echo "========================================================"
echo
read -rp "Pressione ENTER para fechar..."