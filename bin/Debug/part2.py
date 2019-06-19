import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
#s.bind((socket.gethostname(), 1024))
while True:
    a =raw_input("Input:")
    s.sendto(a, socket.INADDR_ANY)