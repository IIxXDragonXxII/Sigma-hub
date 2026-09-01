@echo off
setlocal

echo ========================================================
echo  INSTALADOR DE BIBLIOTECAS - SIGMA HUB
echo ========================================================
echo.

:: Verifica Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale o Python e tente novamente.
    pause
    exit /b 1
)
python --version
echo.

:: Verifica pip
echo [2/5] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] pip nao encontrado. Tente reinstalar o Python.
    pause
    exit /b 1
)
echo.

:: Cria venv se não existir
echo [3/5] Criando ambiente virtual (venv)...
if not exist "venv\" (
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar a venv.
        pause
        exit /b 1
    )
    echo Ambiente virtual criado.
) else (
    echo Ambiente virtual ja existe.
)
echo.

:: Ativa venv e instala bibliotecas
echo [4/5] Instalando bibliotecas...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar a venv.
    pause
    exit /b 1
)

echo Atualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install customtkinter Pillow opencv-python pygame flask

if errorlevel 1 (
    echo [ERRO] Falha na instalacao de alguma biblioteca.
    pause
    exit /b 1
)

:: Gera requirements.txt
echo [5/5] Gerando requirements.txt...
pip freeze > requirements.txt
echo requirements.txt atualizado.

echo.
echo ========================================================
echo  INSTALACAO CONCLUIDA COM SUCESSO!
echo  Todas as bibliotecas estao prontas.
echo  Agora execute o arquivo: iniciar.bat
echo ========================================================
echo.
pause