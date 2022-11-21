import socket
porta_servidor = 6000
hostname = socket.getsockname()
ip_address = socket.gethostbyname(hostname)