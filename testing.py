import time

import ClienteRegistro
import threading


def libera_espera():
    print("func espera")
    clienteObj.libera_thread()


clienteObj = ClienteRegistro.Cliente()
clientThread = threading.Thread(target=clienteObj.iniciar_cliente, args=('lol', 'localhost', 5000)).start()


time.sleep(2)
libera_espera()

time.sleep(10)
libera_espera()

time.sleep(10)
print(clienteObj.get_ultima_consulta())