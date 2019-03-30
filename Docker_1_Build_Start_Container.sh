#!/bin/sh
#create folder to share between host and container (one directory above the folder containing this script)
mkdir ./../files_for_SESToPy
#run a container from the image -> the /app folder in the container is shared with this folder on the host (where the program is), another folder for files for the program is linked as well
docker run --name=sestopycontainer -it -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/app -v $(pwd)/../files_for_SESToPy:/files_from_host -e DISPLAY=$DISPLAY -u qtuser hf/sestopy python3 /app/main.py
