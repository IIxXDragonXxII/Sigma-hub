@echo off
setlocal

echo Iniciando SIGMA HUB...

:: Verifica se a venv existe
if not exist "venv\" (
    echo.
    echo [ERRO] A pasta 'venv' nao foi encontrada.
    echo Execute primeiro o arquivo: instalar_bibliotecas.bat
    echo.
    pause
    exit /b 1
)

:: Ativa a venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao ativar o ambiente virtual.
    echo.
    pause
    exit /b 1
)

:: Executa o programa
python main.py
if errorlevel 1 (
    echo.
    echo [ERRO] O programa foi encerrado com erro.
    echo.
    pause
    exit /b 1
)

:: Se chegou aqui, terminou normalmente
echo.
echo Programa finalizado. Pressione qualquer tecla para fechar.
pause