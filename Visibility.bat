@echo off
if "%1" =="" (goto A) else (goto B) 

:A
echo Please specify the path of the configuration file config.json!
pause
exit

:B
call activate base
python ./b_analysis/main.py "%1"
echo End all
pause
exit