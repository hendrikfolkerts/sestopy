# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'

import os
import socket
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot)
import time

class socketClient(QObject):

    #signals
    clientreturndataSignal = pyqtSignal(str)    #this signal takes a string to transport received data
    clientConnectionSignal = pyqtSignal(bool)   #this signal takes one bool argument
    clientNoSendSignal = pyqtSignal()           #this signal takes no argument

    def __init__(self):
        super(socketClient, self).__init__()
        self.s = None
        self.serverIP = ""
        self.serverPort = 0
        self.sendstring = ""

    def clientSend(self):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = False
        oldsendstring = ""

        while 1:
            if not connection and self.serverIP != "" and self.serverPort != 0:
                try:
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.connect((self.serverIP, self.serverPort))
                    self.clientConnectionSignal.emit(True)
                    connection = True
                    if self.sendstring != "":
                        oldsendstring = self.sendstring
                        try:
                            self.s.sendall(self.sendstring.encode())
                            # receiveddata = self.s.recv(1024).decode()
                            # self.clientreturndataSignal.emit(receiveddata)
                        except:
                            pass
                except:
                    self.serverIP = ""
                    self.serverPort = 0
                    self.clientConnectionSignal.emit(False)
            if connection and self.serverIP != "" and self.serverPort != 0 and self.sendstring != "" and self.sendstring != oldsendstring:
                oldsendstring = self.sendstring
                try:
                    self.s.sendall(self.sendstring.encode())
                    #receiveddata = self.s.recv(1024).decode()
                    #self.clientreturndataSignal.emit(receiveddata)
                except:
                    self.serverIP = ""
                    self.serverPort = 0
                    self.clientNoSendSignal.emit()
            if connection and self.serverIP == "" and self.serverPort == 0:
                self.s.close()
                connection = False

            time.sleep(1)
