@echo off

REM Create output directory if it doesn't exist
if not exist docs\doxygen\output mkdir docs\doxygen\output

REM Run Doxygen
doxygen docs\doxygen\Doxyfile

REM Check if Doxygen ran successfully
if %ERRORLEVEL% EQU 0 (
    echo Documentation generated successfully!
    echo You can find the documentation in docs\doxygen\output\html\index.html
) else (
    echo Error generating documentation
    exit /b 1
) 