@echo off
echo ================================================
echo     GERANDO VERSAO PORTABLE - GERADOR CSRF
echo ================================================

echo.
echo Ativando ambiente virtual...
call .\.venv\Scripts\activate

echo.
echo Limpando pastas antigas...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo.
echo Gerando executavel portable com PyInstaller...
python -m PyInstaller GeradorCSRF.spec --noconfirm

echo.
echo Copiando build final para a pasta:
echo      Gerador_Comprovantes_Portable
rmdir /s /q Gerador_Comprovantes_Portable 2>nul
mkdir Gerador_Comprovantes_Portable
xcopy /e /i /y dist\GeradorCSRF Gerador_Comprovantes_Portable\GeradorCSRF\

echo.
echo ================================================
echo    BUILD FINALIZADO! 
echo    ARQUIVO: Gerador_Comprovantes_Portable\GeradorCSRF\GeradorCSRF.exe
echo ================================================
pause