import json
from socket import *
import threading
import time
import pyaudio
import ClienteRegistro
from estado import Estado
import constantes_conexao as cc
import constantes_audio as ac


class app():
    def __init__(self):
        self.clienteObj = ClienteRegistro.Cliente()
        self.clienteRegistro = '' 
        self.serverUDP = socket(AF_INET, SOCK_DGRAM)
        self.serverUDP.bind((cc.meu_ip, cc.minha_porta))
        self.ThreadEscuta = ''
        self.ThreadFala = ''
        self.estado = Estado.LOGANDO
        self.run()

    
    def run(self):

        print("Insira o seu nome: ")
        self.nome = input()
        self.clienteRegistro = threading.Thread(target= self.clienteObj.iniciar_cliente, args=(self.nome, 'localhost', 5000, cc.meu_ip, cc.minha_porta)).start()
        #Posso receber convites
        self.estado = Estado.LIVRE
        #Thread que escuta convites
        self.ThreadEscuta = threading.Thread(target= self.escuta, args =(self.serverUDP))
        self.menu()


    def menu(self):
        time.sleep(3)
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
        if dados != "Por favor escolha outro nome" and dados != '':
            mensagem = json.loads(dados)
        mensagem = ''
        
        # Enquanto não convidei ninguém, verifico se convidei, ou se fui convidado 
        while "ip" not in mensagem:
            dados = self.clienteObj.get_ultima_consulta()
            if dados != "Por favor escolha outro nome" and dados != '':
                if dados != "Pessoa nao encontrada":
                    mensagem = json.loads(dados)
            if "ip" not in mensagem:
                self.clienteObj.libera_thread()
        self.envia_convite(mensagem)

    def aguarda(self):
        self.estado = Estado.CONVIDADO

        
        

################################################################################################    # 
    
    def escuta(self, server):
        py_audio = py_audio.PyAudio()
        output_stream = py_audio.open(ac.SETTINGS)
        
        while True:
            dados = server.recv(ac.BUFFER).decode("utf-8")
            mensagem = json.loads(dados)
            if self.estado == Estado.LIVRE:
                if mensagem['mensagem'] == 'CONVITE':
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
                if mensagem['mensagem'] == "ACEITO":
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
                if mensagem['mensagem'] == "AUDIO":
                    output_stream.write(mensagem['dados'])
                elif mensagem['mensagem'] == "ENCERRAR_CHAMADA":
                    self.estado = Estado.LIVRE
                    self.menu()
                else:
                    mensagem = {"mensagem":"RECUSADO"}
                    self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))


################################################################################################################
        
    def servidor_envio(self, server, enderecoContato, portaContato):
        server.connect((enderecoContato, portaContato))
        py_audio = pyaudio.PyAudio()
        input_stream = py_audio.open(ac.SETTINGS)
        while self.estado == Estado.OCUPADO:
            data = input_stream.read(ac.BUFFER, exception_on_overflow=False)
            mensagem = { "mensagem": "AUDIO", "dados": data}
            self.server.send(bytes(json.dumps(mensagem), encoding="utf-8"))
        mensagem = {"mensagem":"ENCERRAR_CHAMADA"}
        self.server.send(bytes(json.dumps(mensagem), encoding="utf-8"))

    
    def envia_convite(self, dados):
        self.estado = Estado.CONVIDANDO
        endereco = dados['ip']
        porta = dados['porta']
        mensagem = {
            'mensagem': 'CONVITE',
            'dados': {
                'nome': self.nome,
                'IP': cc.meu_ip,
                'port': cc.minha_porta 
            }
        }
        self.serverUDP.connect((endereco, porta))
        self.serverUDP.send(bytes(json.dumps(mensagem), encoding="utf-8"))

        
if __name__ == '__main__':
    app()
        

