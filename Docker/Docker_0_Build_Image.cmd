@echo off
REM go to this directory
pushd "%~dp0"
REM build the image
docker build -t hf/sestopy .

pause