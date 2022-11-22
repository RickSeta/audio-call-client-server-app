import json
from socket import *
import threading
import time
import pyaudio
import ClienteRegistro
from estado import Estado
import constantes_conexao as cc
import constantes_audio as ac
import random


class app():
    def __init__(self):
        self.clienteObj = ClienteRegistro.Cliente()
        self.clienteRegistro = '' 
        self.serverUDP = socket(AF_INET, SOCK_DGRAM)
        self.clientIP = cc.meu_ip
        self.clientPort = cc.minha_porta + random.randint(0,100)
        self.serverUDP.bind((self.clientIP, self.clientPort))
        self.ThreadEscuta = ''
        self.ThreadFala = ''
        self.estado = Estado.LOGANDO
        self.liberaMenu = True
        self.run()

    
    def run(self):

        print("Insira o seu nome: ")
        self.nome = input()
        self.clienteRegistro = threading.Thread(target= self.clienteObj.iniciar_cliente, args=(self.nome, 'localhost', 5000, self.clientIP, self.clientPort)).start()
        self.clienteObj.libera_thread()

        
        #Posso receber convites
        self.estado = Estado.LIVRE
        #Thread que escuta convites
        self.ThreadEscuta = threading.Thread(target= self.escuta, args =(self.serverUDP,)).start()
        self.menu()


    def menu(self):
        mensagem = ''
        print("while libera menu")
        while self.liberaMenu:
            dados = self.clienteObj.get_ultima_consulta()
            if dados["mensagem"] == "Usuario registrado!":
                self.liberaMenu = False
        print("Para convidar alguem, envie 1")
        print("Para esperar um convite, envie 2")
        opcao = int(input())
        while opcao != 1 and opcao != 2:
            opcao = input()
        if opcao == 1:
            self.convida()
        else:
            self.aguarda()



    def convida(self):
        self.clienteObj.libera_thread()
        dados = self.clienteObj.get_ultima_consulta()
        mensagem = dados['mensagem']
        # Enquanto não convidei ninguém, verifico se convidei, ou se fui convidado 
        while mensagem != "consulta":
            dados = self.clienteObj.get_ultima_consulta()
            mensagem = dados['mensagem']
        self.clienteObj.libera_thread()
        self.envia_convite(dados)

    def aguarda(self):
        print("Esperando um convite ...")

        
        

################################################################################################    # 
    
    def escuta(self, server):
        py_audio = pyaudio.PyAudio()
        output_stream = py_audio.open(format=ac.FORMAT, output=True, rate=ac.RATE, channels=ac.CHANNELS,
                                      frames_per_buffer=ac.BUFFER)
        print("def escuta")
        while True:
            dados = server.recv(ac.BUFFER).decode("utf-8")
            mensagem = json.loads(dados)
            if self.estado == Estado.LIVRE:
                print("def escuta estado livre")
                if mensagem['mensagem'] == 'CONVITE':
                    print("def escuta estado livre mensagem convite")
                    self.estado == Estado.CONVIDADO
                    enderecoContato = mensagem['dados']['ip']
                    portaContato = mensagem['dados']['port']
                    print(mensagem['dados']['nome'] + "quer iniciar uma chamada")
                    print("Para aceitar a chamada, envie s")
                    print("Para recusar a chamada, envie n")
                    resposta = input()
                    while resposta != 's' and resposta != 'n':
                        resposta = input()
                    if resposta == 's':
                        mensagem = {"mensagem":"ACEITO"}
                        self.estado = Estado.OCUPADO
                        self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))
                        self.ThreadFala = threading.Thread(target=self.servidor_envio, args=(enderecoContato, portaContato))
                        self.ThreadFala.start()

                    if resposta == 'n':
                        self.estado = Estado.LIVRE
                        mensagem = {"mensagem": "RECUSADO"}
                        self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))
                        self.menu()


            if self.estado == Estado.CONVIDANDO:
                print("def escuta convidado")
                if mensagem['mensagem'] == "ACEITO":
                    print("def escuta convidado mensagem aceito")
                    self.estado = Estado.OCUPADO
                    enderecoContato = mensagem['dados']['ip']
                    portaContato = mensagem['dados']['porta']
                    self.ThreadFala = threading.Thread(target=self.envia_audio, args=(server, enderecoContato, portaContato))
                    self.ThreadFala.start()
                    # cria thread de envio
                elif mensagem['mensagem'] == 'RECUSADO':
                    self.estado = Estado.LIVRE
                    self.menu()
                    
            if self.estado == Estado.OCUPADO:
                print("def escuta ocupado")
                if mensagem['mensagem'] == "AUDIO":
                    output_stream.write(mensagem['dados'])
                elif mensagem['mensagem'] == "ENCERRAR_CHAMADA":
                    self.estado = Estado.LIVRE
                    self.menu()
                else:
                    mensagem = {"mensagem":"RECUSADO"}
                    self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))
            print("while escuta")


################################################################################################################
        
    def servidor_envio(self, server, enderecoContato, portaContato):
        server.connect((enderecoContato, portaContato))
        py_audio = pyaudio.PyAudio()
        input_stream = py_audio.open(format=ac.FORMAT, output=True, rate=ac.RATE, channels=ac.CHANNELS,
                                      frames_per_buffer=ac.BUFFER)
        while self.estado == Estado.OCUPADO:
            data = input_stream.read(ac.BUFFER, exception_on_overflow=False)
            mensagem = { "mensagem": "AUDIO", "dados": data}
            self.server.send(bytes(json.dumps(mensagem), encoding="utf-8"))
        mensagem = {"mensagem":"ENCERRAR_CHAMADA"}
        self.server.send(bytes(json.dumps(mensagem), encoding="utf-8"))

    
    def envia_convite(self, dados):
        self.estado = Estado.CONVIDANDO
        endereco = dados['dados']['ip']
        porta = dados['dados']['porta']
        mensagem = {
            'mensagem': 'CONVITE',
            'dados': {
                'nome': self.nome,
                'ip': self.clientIP,
                'port': self.clientPort
            }
        }
        print("connect server udp")
        self.serverUDP.connect((endereco, porta))
        self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))

        
if __name__ == '__main__':
    try:    #agora começa o loop de evento
        app()
    except KeyboardInterrupt:
        print("Crtl+C pressionado, fechando servidor")    

