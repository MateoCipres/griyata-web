@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo === Publicar el catalogo de Griyata Parfums ===
echo.

echo 1/4  Trayendo los cambios de la planilla de Google (en GitHub)...
set "prev="
for /f %%i in ('gh run list --workflow actualizar.yml --limit 1 --json databaseId -q ".[0].databaseId" 2^>nul') do set "prev=%%i"
gh workflow run actualizar.yml >nul 2>&1
if errorlevel 1 (
  echo      No pude lanzar la actualizacion desde la planilla. Sigo con el resto.
  goto local
)
set "run=%prev%"
set /a intentos=0
:esperar
ping -n 4 127.0.0.1 >nul
set /a intentos+=1
for /f %%i in ('gh run list --workflow actualizar.yml --limit 1 --json databaseId -q ".[0].databaseId" 2^>nul') do set "run=%%i"
if "%run%"=="%prev%" if %intentos% lss 20 goto esperar
if "%run%"=="%prev%" (
  echo      GitHub no arranco la actualizacion a tiempo. Sigo con el resto.
  goto local
)
gh run watch %run% --exit-status >nul 2>&1
if errorlevel 1 (
  echo      La actualizacion desde la planilla fallo. Mira la pestana Actions en GitHub.
) else (
  echo      Planilla al dia.
)

:local
echo.
echo 2/4  Bajando la ultima version y armando la pagina...
git pull -q --rebase --autostash
if errorlevel 1 goto error
python armar.py
if errorlevel 1 goto error

git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo.
  echo No hay otros cambios para publicar.
  echo Lo de la planilla ya se publica solo. En uno o dos minutos se ve en:
  echo https://mateocipres.github.io/griyata-web/
  goto fin
)

echo.
set "msg="
set /p "msg=3/4  Que cambiaste? (ej: precios nuevos): "
if "%msg%"=="" set "msg=Actualizacion del catalogo"
git commit -q -m "%msg%"
if errorlevel 1 goto error

echo.
echo 4/4  Subiendo a GitHub...
git push -q
if errorlevel 1 goto error

echo.
echo Listo. En uno o dos minutos se ve en:
echo https://mateocipres.github.io/griyata-web/
goto fin

:error
echo.
echo Algo salio mal. Revisa el mensaje de arriba.

:fin
echo.
pause
