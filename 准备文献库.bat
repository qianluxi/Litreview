@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul 2>nul

rem Keep this file pure ASCII: Chinese bytes + chcp 65001 break cmd's line parsing.
rem Child-process encoding is pinned to UTF-8 inside the wizard.
set "PYCMD="
where python >nul 2>nul
if not errorlevel 1 set "PYCMD=python"
if not defined PYCMD (
  where py >nul 2>nul
  if not errorlevel 1 set "PYCMD=py -3"
)
rem Optional: pin the interpreter that produced the existing corpus.
if defined LITREV_PYTHON set "PYCMD="%LITREV_PYTHON%""
if not defined PYCMD (
  echo [!] Python 3 not found in PATH. Install Python 3.10+ first.
  goto END
)

echo.
%PYCMD% tools\prepare_library.py %*
if errorlevel 1 (
  echo.
  echo [!] Preparation stopped. Read the message above; nothing half-done was left behind.
) else (
  echo.
  echo [OK] Wizard finished. Restart the OpenCode client, then dispatch the ex- agents listed above.
)

:END
echo.
rem No argument = double-click: keep the window open. Command-line use does not block.
if "%~1"=="" pause
endlocal
