import sys
import socket
import selectors
import types

seletor = selectors.DefaultSelector()   # Cria um seletor, elemento reponsavel por cuidar de observaveis


def aceitar_conexao_paralela(sock):
    socketCliente, enderecoCliente = sock.accept()  # Aceita nova conexao retornando o socket e o endereco
    print(f"Conexao aceita de {enderecoCliente}")
    socketCliente.setblocking(False)    # faz com que .accept(), .connect(), .send(), e .recv() não bloqueiem o processo de outros sockets
    data = types.SimpleNamespace(addr=enderecoCliente, inb=b"", outb=b"")   # Cria um objeto customizado com 3 campos, endereço, buffer entrada e buffer saida
    eventosDoCliente = selectors.EVENT_READ | selectors.EVENT_WRITE     #define quais eventos deste cliente observaremos
    seletor.register(socketCliente, eventosDoCliente, data=data)    #registra o socket na lista de observaveis


def service_connection(key, mask):
    socketCliente = key.fileobj
    dados = key.data
    if mask & selectors.EVENT_READ:     #se o evento for de leitura: receber os dados
        recv_data = socketCliente.recv(1024)    #tamanho de dados esperados é de no maximo 1024 bytes
        if recv_data:
            dados.outb += recv_data     # se houver dados escreva no buffer
        else:
            print(f"Fechando conexao para {dados.addr}")    #se nao a principio fecha a conexao visto que o envio foi
            seletor.unregister(socketCliente)               #feito, porém nada no campo de dados
            socketCliente.close()
    if mask & selectors.EVENT_WRITE:    # se o evento for de escrita e houver o que devolver envie os dados
        if dados.outb:
            print(f"Ecoando {dados.outb!r} para {dados.addr}")      #vamos mudar esse comportamento para consulta
            enviados = socketCliente.send(dados.outb)   # a dunfação send envia os dados e retorna quantos bytes enviados
            dados.outb = dados.outb[enviados:]      #essa linha limpa o buffer de envio ate a posição do ultimo byte enviado


host, porta = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #cria um listener socket com ipv4 e tcp
lsock.bind((host, porta))    #seta o 'socket' para um 'host' e uma porta
lsock.listen()  #começar a escutar no 'host' e porta especificados
print(f"Escutando em {(host, porta)}")


lsock.setblocking(False)    #faz com que .accept(), .connect(), .send(), e .recv() não bloqueiem o processo deste socket

# registra o socket na lista de observaveis, tendo como evento trigger o read
seletor.register(lsock, selectors.EVENT_READ, data=None)


try:    #agora começa o loop de evento
    while True:
        events = seletor.select(timeout=None)   #bloqueia e fica esperando para que algum evento registrado ocorra

        # O retorno do .select() é key e mask, key.data tem os dados e key.fileobj tem o socket que ativou um evento
        for key, mask in events:

            # Se não houver dados, quer dizer que o socket retornado é o listener do servidor, trazendo uma nova conexão
            if key.data is None:
                aceitar_conexao_paralela(key.fileobj)

            # Se houver dados, quer dizer que é de uma conexão já existente com algum cliente
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Crtl+C pressionado, fechando servidor")
finally:
    seletor.close()
