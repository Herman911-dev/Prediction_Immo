@echo off
echo ===================================================
echo LANCEMENT DU PIPELINE CI/CD (Mise a jour globale)
echo ===================================================
 
echo.
echo [1/4] INGESTION DES NOUVELLES DONNEES...
python src/ingestion.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [2/4] MISE A JOUR DE LA BASE DE DONNEES POSTGRESQL...
python src/to_sql.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [3/4] RE-ENTRAINEMENT DE L'INTELLIGENCE ARTIFICIELLE...
python src/train.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [4/4] REDEMARRAGE DE L'APPLICATION STREAMLIT (DOCKER)...
docker-compose restart app

echo.
echo ===================================================
echo MISE A JOUR TERMINEE ! L'application est a jour.
echo ===================================================
pause