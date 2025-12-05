@echo off
chcp 65001 > nul
title AnimeCut - Cortes Automáticos para Animes

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🎌 ANIMECUT - CORTES AUTOMÁTICOS PARA ANIMES     ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo [INFO] Iniciando AnimeCut...
echo.

REM Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo [INFO] Instale Python 3.8+ de https://www.python.org/
    pause
    exit /b 1
)

REM Verifica se as dependências estão instaladas
echo [INFO] Verificando dependências...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Dependências não instaladas. Instalando...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências!
        pause
        exit /b 1
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  ✅ AnimeCut está pronto!                                ║
echo ║                                                          ║
echo ║  🌐 Abrindo navegador...                                 ║
echo ║  📱 Interface otimizada para animes                      ║
echo ║  🎨 Preservação de qualidade premium                     ║
echo ║  🎵 Detecção automática de Opening/Ending                ║
echo ║                                                          ║
echo ║  Para parar: Pressione Ctrl+C                            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Inicia o Streamlit
streamlit run app.py --server.headless=false

pause
