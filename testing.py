import time

import ClienteRegistro
import threading


def espera():
    clienteObj.libera_thread()


clienteObj = ClienteRegistro.Cliente()
clientThread = threading.Thread(target=clienteObj.iniciar_cliente, args=('lol', 'localhost', 5000)).start()

espera()

time.sleep(15)
espera()

