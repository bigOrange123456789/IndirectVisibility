@echo off
if "%1" =="" (goto A) else (goto B) 

:A
echo Please specify the path of the configuration file config.json!
pause
exit

:B
call activate myOpenGL2
python ./src_obj/mainGPU.py "%1"
python ./src_py/main.py "%1"
echo End all
pause
exit