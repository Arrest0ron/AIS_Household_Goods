@echo off
chcp 65001 >nul
call .venv\Scripts\activate.bat

pyinstaller --onefile --windowed ^
    --name "AIS_Shop" ^
    --icon resources\app.ico ^
    --add-data "resources;resources" ^
    --hidden-import psycopg2 ^
    --hidden-import matplotlib ^
    --hidden-import matplotlib.backends.backend_qtagg ^
    --collect-submodules matplotlib ^
    main.py

echo.
echo Готово! .exe в папке dist\AIS_Shop.exe
pause
