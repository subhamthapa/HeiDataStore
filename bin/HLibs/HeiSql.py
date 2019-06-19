import socket
import os
import sys
class HeiSql:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9191
        os.system("color 37")

    def send_hsql(self):
        self.socket.connect((self.host, self.port))
        while True:
            sql = raw_input("HSql/>")
            if sql == "clear":
                os.system("cls")
                continue
            self.socket.send(sql)
            print ""
            print self.socket.recv(1024)
            print ""

os.system("title HeiSQL console")
HeiSql().send_hsql()