# echo-client.py
import json
import selectors
import socket
import sys
import threading
from datetime import time

import registroLib
messages = [b"Message 1 from client.", b"Message 2 from client."]


class Cliente:

    def __init__(self):
        self._condition_espera = threading.Condition()
        self._condition_func = threading.Condition()

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 5000  # The port used by the server

    def libera_thread(self):
        self._condition_espera.acquire()
        self._condition_espera.notify_all()
        self._condition_espera.release()

    def iniciar_cliente(self, nome_inicial, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Socket iniciado na porta " + str(s.getsockname()), flush=True)
        manager = registroLib.Pacote(s)
        try:
            nome = nome_inicial
            primeira = True
            aberto = True
            registro = True
            while aberto:

                if registro:
                    registro = False
                    if primeira:
                        s.connect((host, int(port)))
                        primeira = False
                    m = {"nome": nome, "tipo-pedido": 'r'}
                else:
                    try:
                        self._condition_espera.acquire()
                        self._condition_espera.wait()
                    finally:
                        self._condition_espera.release()
                    consultaTipo = input('Digite c para consultar um ip ou f para finalizar: ')
                    manager.tipo_req = ""
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
                print(f"Recebido {data!r}")
                if data == "Por favor escolha outro nome":
                    nome = input("Novo nome: ")
                    registro = True
            print("Cliente finalizando")
        except KeyboardInterrupt:
            print("Crtl+C pressionado, fechando servidor")

