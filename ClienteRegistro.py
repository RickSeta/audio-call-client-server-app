# echo-client.py
import json
import selectors
import socket
from datetime import time

import registroLib
messages = [b"Message 1 from client.", b"Message 2 from client."]


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = registroLib.Pacote(sel, sock)
        sel.register(sock, events, data=message)


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        nome = input("Qual seu nome? ")
        primeira = True
        aberto = True
        while aberto:

            if primeira:
                s.connect((HOST, PORT))
                primeira = False
                m = {"nome": nome, "tipo-pedido": 'r'}
            else:
                consultaTipo = input("f para fechar e c para consulta: ")
                if consultaTipo == 'c':
                    m = {"nome": nome, "tipo-pedido": consultaTipo, "consulta": input("Qual nome do usuario a consultar?")}
                elif consultaTipo == 'f':
                    print("Encerrando cliente!")
                    aberto = False
                    m = {"nome": nome, "tipo-pedido": consultaTipo}

            data = json.dumps(m)
            num = s.send(bytes(data, encoding="utf-8"))
            print("data " + data)
            data = s.recv(len(data)+10).decode("utf-8")
            print(f"Received {data!r}")

    except KeyboardInterrupt:
        print("Crtl+C pressionado, fechando servidor")

