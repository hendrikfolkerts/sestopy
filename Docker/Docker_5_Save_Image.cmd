@echo off
REM save the image
cd %HOMEPATH%
docker save -o SESToPy_Docker_Image.tar hf/sestopy

pause