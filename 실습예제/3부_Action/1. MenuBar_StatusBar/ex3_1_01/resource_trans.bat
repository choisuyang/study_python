@echo off
set /p str=input file name?(*.qrc)

pyrcc5 %str%.qrc -o %str%_rc.py
pause