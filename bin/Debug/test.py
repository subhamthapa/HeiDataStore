import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind((socket.gethostname(), 1024))
#s.listen(5)
str = ""
while True:
    print s.recvfrom(1024)