@echo off
set path0="%1"
if %path0% =="" (goto A) else (goto B) 

:A
set path0=start_config.json
echo Please specify the path of the configuration file config.json!
echo Because you did not enter the file path, now use the test file: %path0%
echo Press any key to continue!
pause

:B
call activate myOpenGL2
python ./a_sampling/mainGPU.py %path0%
python ./b_analysis/main.py %path0%
echo End all
pause
exit