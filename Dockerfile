FROM ubuntu:latest

MAINTAINER hendrikfolkerts <hendrikmartinfolkerts@gmail.com>

# Add user
RUN adduser --quiet --disabled-password qtuser

# Install Python 3 and PyQt5
RUN apt-get update
RUN apt-get install -y python3 python3-pyqt5