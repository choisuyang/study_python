@echo off
set /p str=input file name?(*.ui)

pyrcc5 %str%.qrc -o %str%_rc.py
pause