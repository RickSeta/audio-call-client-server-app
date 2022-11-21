from socket import *

import threading
import pyaudio
import json


import audio_constants as ac
import socket_constants as cc
import helpers
from estado import Estado


class app():
    def __init__(self):
        self.clientTCP = socket(AF_INET, SOCK_STREAM)
        self.clientTCP.setblocking(False)
        self.serverUDP = socket(AF_INET, SOCK_DGRAM)
        self.estado = Estado.LIVRE
        self.login()
    
    
    def login(self): 
        self.clientTCP.connect(cc.ip_address, cc.porta_servidor)   
        while True:
            self.nome = input()
            if (self.nome == "quit"):
                self.clientTCP.close()
                quit()
            else:
                mensagem = {'mensagem':'LOGIN', 'nome':self.nome}
                self.clientTCP.send(json.dumps(mensagem), cc.ip_address, cc.porta_servidor)
                resposta = json.loads(self.clientTCP.recv())
                if resposta['mensagem'] == "ACEITO":
                    break
        
        self.listenThread = threading.Thread(self.escuta, self.serverUDP)
        self.menu()
    

    def sair_da_aplicacao(self):
        mensagem = {"mensagem":"SAIR_DA_APP"}
        self.clientTCP.sendto(json.dumps(mensagem), (cc.ip_address, cc.porta_servidor))
        self.clientTCP.close()
        quit()

        

    def menu(self):
        helpers.limpa_tela()
        self.lista_usuarios()
        while self.estado == Estado.LIVRE:
            self.entrada_do_usuario()

    def entrada_do_usuario (self):
        if self.estado == Estado.LI:
            print("Para iniciar uma ligação com algum usuário, digite o seu nome")
            print('Para sair da aplicação, envie "q"')
            print('Para atualizar a lista de pessoas disponíveis, envie "r"')
            entrada = input()
            if (entrada == 'q'):
                self.sair_da_aplicacao()
            elif (entrada == 'r'):
                self.atualiza_menu()
            else:
                for pessoa in range(len(self.lista)):
                    if entrada in self.lista[pessoa]['nome']:
                        enderecoContato = self.lista[pessoa]['IP']
                        portaContato = self.lista[pessoa]['port']
                        self.envia_pedido(enderecoContato, portaContato)
                        
    def envia_pedido(self, endereco, porta):
        self.estado = Estado.CONVIDANDO
        self.serverUDP.bind(endereco, porta)
        mensagem = {
            'mensagem':'CONVITE',
            'dados':{
                'nome': self.nome,
                'IP': cc.ip_address,
                'port': cc.porta_servidor
            }
        }
        self.serverUDP.sendto(json.dumps(mensagem), endereco, porta)

    
    def escuta(self, server):
        py_audio = py_audio.PyAudio()
        output_stream = py_audio.open(ac.SETTINGS)
        
        while True:
            mensagem = server.recvfrom(ac.BUFFER)
            mensagem = json.loads(mensagem)
            if self.estado == Estado.LIVRE:
                if mensagem['mensagem'] == 'CONVITE':
                    helpers.limpa_tela()
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
                        helpers.limpa_tela()
                        mensagem = {"mensagem":"ACEITO"}
                        self.serverUDP.sendto(json.dumps(mensagem), cc.ip_address, cc.porta_servidor)
                        self.estado = Estado.OCUPADO
                        self.talkThread = threading.Thread(target=self.servidor_envio, args=(enderecoContato, portaContato))
                        thread.start()

                    if resposta == 'n':
                        self.estado = Estado.LIVRE
                        mensagem = {"mensagem": "RECUSADO"}
                        self.serverUDP.sendto(json.dumps(mensagem), _address=(enderecoContato, portaContato))
                        self.atualiza_menu()


            if self.estado == Estado.CONVIDANDO:
                if mensagem['mensagem'] == "ACEITO":
                    self.estado = Estado.OCUPADO
                    thread = threading.Thread(self.envia_audio, 'endereço do contato fudeu')
                    thread.start()
                    # cria thread de envio
                elif mensagem['mensagem'] == 'RECUSADO':
                    self.estado = Estado.LIVRE
                    
            if self.estado == Estado.OCUPADO:
                if mensagem['mensagem'] == "AUDIO":
                    output_stream.write(mensagem['dados'])
                elif mensagem['mensagem'] == "ENCERRAR_CHAMADA":
                    self.estado = Estado.LIVRE
                else:
                    mensagem = {"mensagem":"RECUSADO"}
                    self.serverUDP.sendto(json.dumps(mensagem), _address=(enderecoContato, portaContato))

    
    def servidor_envio(self, enderecoContato, portaContato):
        py_audio = pyaudio.PyAudio()
        input_stream = py_audio.open(ac.SETTINGS)
        while self.estado == Estado.OCUPADO:
            data = input_stream.read(ac.BUFFER, exception_on_overflow=False)
            self.serverUDP.sendto(data, enderecoContato, portaContato)
        self.serverUDP.sendto('ENCERRAR_CHAMADA'.encode(), enderecoContato, portaContato)
        self.atualiza_menu()
        
    
    def atualiza_menu(self):
        self.menu()

    def lista_usuarios(self):
        mensagem = 'LISTAR_USUARIOS'
        self.clientTCP.send(mensagem.encode())
        self.lista = self.clientTCP.recv().decode()
        for usuario in len(self.lista):
            print(self.lista[usuario]['nome'])


