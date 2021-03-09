@echo off
REM delete all containers
FOR /f "tokens=*" %%i IN ('docker ps -aq') DO docker rm %%i
REM delete all images
FOR /f "tokens=*" %%i IN ('docker images --format "{{.ID}}"') DO docker rmi %%i

pause