

@echo off
setlocal
:: esto es un comentario 
:: pinche desmadre de codigo para obtener la fechahora y ponerlo en una variable de nombre _date
:: use findstr to strip blank lines from wmic output
for /f "usebackq skip=1 tokens=1-6" %%g in (`wmic Path Win32_LocalTime Get Day^,Hour^,Minute^,Month^,Second^,Year ^| findstr /r /v "^$"`) do (
  set _day=00%%g
  set _hours=00%%h
  set _minutes=00%%i
  set _month=00%%j
  set _seconds=00%%k
  set _year=%%l
  )
:: pad with leading zeros
set _month=%_month:~-2%
set _day=%_day:~-2%
set _hh=%_hours:~-2%
set _mm=%_minutes:~-2%
set _ss=%_seconds:~-2%
set _date=%_year%_%_month%_%_day%_%_hh%_%_mm%_%_ss%
echo %_date%
:: Utilizar la cadena generada para generar el commit
git add *.py
git add *.bat
git commit -m "%_date%"
:: Actualizar el repositorio 
git push -u origin main

endlocal