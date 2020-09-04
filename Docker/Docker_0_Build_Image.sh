#!/bin/sh
#go to the directory of this script
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#cd $DIR
cd "$(dirname "$0")"
#build the image
docker build -t hf/sestopy .