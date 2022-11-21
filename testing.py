import time

import ClienteRegistro
import threading


def libera_espera():
    print("func espera")
    clienteObj.libera_thread()


clienteObj = ClienteRegistro.Cliente()
clientThread = threading.Thread(target=clienteObj.iniciar_cliente, args=('lol', 'localhost', 5000)).start()


time.sleep(5)
libera_espera()

time.sleep(60)
libera_espera()