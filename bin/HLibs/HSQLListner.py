import socket
import HeiSqlParser
import threading
import os


class HSQLListner:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.host = socket.gethostname()
        self.port = 9191
        self.parser = HeiSqlParser.HeiSqlParser()

    def client_handle(self, client):
        while True:
            try:
                Hsql = client.recv(1024)
                if Hsql == "close":
                    client.close
                    self.socket.close
                print Hsql
                ret = self.parser.hsql(Hsql)
                client.send(str(ret))
            except KeyError:
                client.send("SQL not understandable.")
            except Exception:
                print "Connection Closed"
                break

    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        while True:
            c, addr = self.socket.accept()
            c_thread = threading.Thread(target=self.client_handle, args=(c,))
            c_thread.start()

os.system("title HSQL Listner")
HSQLListner().start_server()
