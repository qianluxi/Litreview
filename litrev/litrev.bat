@echo off
chcp 936 >nul 2>nul
setlocal enabledelayedexpansion
pushd "%~dp0"

rem ============================================================
rem  文献综述流水线 · 简易启动器
rem  双击运行 = 菜单；把 .md / .xlsx 拖到本文件上 = 直接校验
rem  litrev.bat 2 = 直接执行第 2 项，不进入菜单
rem ============================================================

set "NOTES=..\notes"
set "DRAFT=%NOTES%\文献综述_初稿_v1.md"
set "P2=%NOTES%\文献对比与系统特征表2.xlsx"
set "P3=%NOTES%\P3_度量汇总_补全版.xlsx"

rem ---------- 找 Python ----------
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY (
  where py >nul 2>nul && set "PY=py -3"
)
if not defined PY (
  echo.
  echo  [x] 没找到 Python。请安装 Python 3.9+ 并勾选 "Add python.exe to PATH"。
  echo.
  pause
  exit /b 1
)

rem ---------- 依赖 ----------
%PY% -c "import pymupdf, openpyxl" >nul 2>nul
if errorlevel 1 (
  echo.
  echo  [!] 缺少依赖，正在安装 pymupdf 与 openpyxl ...
  %PY% -m pip install --quiet pymupdf openpyxl
  %PY% -c "import pymupdf, openpyxl" >nul 2>nul
  if errorlevel 1 (
    echo  [x] 安装失败。请手动执行：%PY% -m pip install pymupdf openpyxl
    pause
    exit /b 1
  )
)

rem ---------- 入口分派：数字→直通（先判）；有参且文件存在→拖拽；无参→菜单 ----------
if "%~1"=="" goto menu
set "A=%~1"
if "!A!"=="1" ( set "ONESHOT=1" & goto do_index )
if "!A!"=="2" ( set "ONESHOT=1" & goto do_verify )
if "!A!"=="3" ( set "ONESHOT=1" & goto do_p2 )
if "!A!"=="4" ( set "ONESHOT=1" & goto do_p3 )
if "!A!"=="5" ( set "ONESHOT=1" & goto do_locate )
if "!A!"=="6" ( set "ONESHOT=1" & goto do_doc )
if exist "%~1" goto drag

echo.
echo  [x] 参数无法识别：%~1
echo      用法：双击运行；或把 .md / .xlsx 拖到本文件上；或 litrev.bat 1..6
timeout /t 3 >nul
goto menu

rem ============================================================
:menu
cls
echo.
echo  ==========================================================
echo    文献综述流水线   litrev
echo  ==========================================================
echo.
if exist "_index\corpus.json.gz" (
  for %%A in ("_index\corpus.json.gz") do echo    索引：%%~tA
) else (
  echo    索引：尚未建立，请先按 1
)
echo.
echo    [1] 建索引          PDF 有增删后运行，约 10 秒
echo    [2] 核验综述初稿     引文逐字 / 页码 / 出处，并出 xlsx
echo    [3] 校验证据矩阵     P2，应为 22 行
echo    [4] 校验度量表       P3 子集表，允许不覆盖全部文献
echo    [5] 回查一段引文     粘贴英文原句，返回文件与页码
echo    [6] 打开流程说明     PIPELINE.md
echo    [0] 退出
echo.
set "c="
set /p "c=  请选择 [0-6]: "
if not defined c goto end
if "!c!"=="1" goto do_index
if "!c!"=="2" goto do_verify
if "!c!"=="3" goto do_p2
if "!c!"=="4" goto do_p3
if "!c!"=="5" goto do_locate
if "!c!"=="6" goto do_doc
if "!c!"=="0" goto end
goto menu

rem ============================================================
:need_index
if exist "_index\corpus.json.gz" exit /b 0
echo.
echo   [!] 还没有索引，先建一次 ...
%PY% litrev.py index
echo.
exit /b 0

rem ============================================================
:do_index
cls
echo.
echo  --- 建索引 ---
echo.
%PY% litrev.py index
echo.
if defined ONESHOT goto end
pause
goto menu

rem ============================================================
:do_verify
call :need_index
cls
echo.
echo  --- 核验引文 ---
echo  文件：%DRAFT%
echo.
if not exist "%DRAFT%" (
  echo  [x] 找不到该文件。可把 .md 拖到本 bat 上，或改脚本里的 DRAFT 变量。
  if defined ONESHOT goto end
  pause
  goto menu
)
%PY% litrev.py verify "%DRAFT%" --xlsx
echo.
if defined ONESHOT goto end
pause
goto menu

rem ============================================================
:do_p2
call :need_index
cls
echo.
echo  --- 校验证据矩阵 P2（应 22 行）---
echo.
if not exist "%P2%" (
  echo  [x] 找不到：%P2%
  if defined ONESHOT goto end
  pause
  goto menu
)
%PY% litrev.py matrix "%P2%"
echo.
if defined ONESHOT goto end
pause
goto menu

rem ============================================================
:do_p3
call :need_index
cls
echo.
echo  --- 校验度量表 P3（子集表）---
echo.
if not exist "%P3%" (
  echo  [x] 找不到：%P3%
  if defined ONESHOT goto end
  pause
  goto menu
)
%PY% litrev.py matrix "%P3%" --allow-subset
echo.
if defined ONESHOT goto end
pause
goto menu

rem ============================================================
:do_locate
call :need_index
cls
echo.
echo  --- 回查引文 ---
echo  粘贴英文原句（不要带引号），回车执行；直接回车返回菜单。
echo.
set "q="
set /p "q=  > "
if not defined q goto menu
%PY% litrev.py locate "!q!"
echo.
if defined ONESHOT goto end
pause
goto menu

rem ============================================================
:do_doc
if exist "PIPELINE.md" (
  start "" "PIPELINE.md"
) else (
  echo  [x] 找不到 PIPELINE.md
  pause
)
goto menu

rem ============================================================
:drag
set "F=%~1"
if /i "%~x1"==".md" goto drag_md
if /i "%~x1"==".xlsx" goto drag_xlsx
goto drag_text

:drag_md
call :need_index
cls
echo.
echo  --- 核验引文：%~nx1 ---
echo.
%PY% litrev.py verify "%F%" --xlsx
echo.
pause
goto end

:drag_xlsx
call :need_index
cls
echo.
echo  --- 校验表格：%~nx1 ---
echo  若为子集表，改用菜单第 4 项可跳过「必须覆盖全部文献」的检查。
echo.
%PY% litrev.py matrix "%F%"
echo.
pause
goto end

:drag_text
call :need_index
cls
echo.
echo  --- 回查：%F% ---
echo.
%PY% litrev.py locate "%F%"
echo.
pause
goto end

rem ============================================================
:end
if not defined ONESHOT (
  echo.
  echo   已退出。
  echo   按任意键关闭窗口 ...
  pause >nul
)
popd
endlocal
exit /b 0
