@echo off
chcp 65001 >nul
call .venv\Scripts\activate.bat

pyinstaller --onefile --windowed ^
    --name "AIS_Shop" ^
    --icon resources\app.ico ^
    --add-data "resources;resources" ^
    --hidden-import psycopg2 ^
    main.py

echo.
echo Готово! .exe в папке dist\AIS_Shop.exe
pause
