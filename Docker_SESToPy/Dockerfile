FROM ubuntu:18.04

MAINTAINER hendrikfolkerts <hendrikmartinfolkerts@gmail.com>

# Add user
RUN adduser --quiet --disabled-password qtuser

# Install Python 3, PyQt5, and nano as editor
RUN apt-get update
RUN apt-get install -y python3 python3-pyqt5 nano

#copy the program in this folder in the /app folder
COPY . /app

#changes the ownership of the /app folder to qtuser (non-root user)
RUN chown -R qtuser /app
USER qtuser
