@echo off
if "%1" =="" (goto A) else (goto B) 

:A
echo Please specify the path of the configuration file config.json!
pause
exit

:B
call activate base
python ./a10/1.0check.py "%1"
python ./a10/2.0merge.py "%1"
python ./b_analysis/main.py "%1"
echo End all
pause
exit