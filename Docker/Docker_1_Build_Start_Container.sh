#!/bin/sh
#create folder to share between host and container (one directory above the folder containing this script)
mkdir ./../files_for_SESToPy
#run a container from the image -> the program is in the /app folder where it is started from, a folder for files for the program is linked as well
docker run --name=sestopycontainer -it -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd)/../files_for_SESToPy:/files_from_host -e DISPLAY=$DISPLAY -u qtuser hf/sestopy python3 /app/main.py
