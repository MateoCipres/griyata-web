@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo === Publicar el catalogo de Griyata Parfums ===
echo.

echo 1/3  Bajando la ultima version y armando la pagina...
git pull -q --rebase --autostash
if errorlevel 1 goto error
python armar.py
if errorlevel 1 goto error

git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo.
  echo No hay cambios para publicar.
  goto fin
)

echo.
set "msg="
set /p "msg=2/3  Que cambiaste? (ej: precios nuevos): "
if "%msg%"=="" set "msg=Actualizacion del catalogo"
git commit -q -m "%msg%"
if errorlevel 1 goto error

echo.
echo 3/3  Subiendo a GitHub...
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
