import sys
import socket
import selectors
import registroLib

from _thread import *
import threading

print_lock = threading.Lock()

listaUsuarios = {}


def aceitar_conexao_paralela(sock):
    socketCliente, enderecoCliente = sock.accept()  # Aceita nova conexao retornando o socket e o endereco
    print(f"Conexao aceita de {enderecoCliente}")
    socketCliente.setblocking(False)    # faz com que .accept(), .connect(), .send(), e .recv() não bloqueiem o processo de outros sockets
    manager = registroLib.Pacote(socketCliente, enderecoCliente, listaUsuarios)
    start_new_thread(service_connection, (manager,))


def service_connection(manager):
    manager.processar_recebimento()
    print("========================")


host, porta = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #cria um listener socket com ipv4 e tcp
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, porta))    #seta o 'socket' para um 'host' e uma porta


#lsock.setblocking(False)    #faz com que .accept(), .connect(), .send(), e .recv() não bloqueiem o processo deste socket

try:    #agora começa o loop de evento
    while True:
        print(f"Escutando em {(host, porta)}")
        lsock.listen()  #começar a escutar no 'host' e porta especificados
        # O retorno do .select() é key e mask, key.data tem os dados e key.fileobj tem o socket que ativou um evento
        aceitar_conexao_paralela(lsock)
except KeyboardInterrupt:
    print("Crtl+C pressionado, fechando servidor")
