@echo off
set /p str=input file name?(*.ui)

del %str%.py
python -m PyQt5.uic.pyuic -x %str%.ui -o %str%.py
pause