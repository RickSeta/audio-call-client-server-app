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
        self.endereco = self.serverUDP.getsockname()[0]
        self.porta = self.serverUDP.getsockname()[1]
        self.ThreadEscuta = ''
        self.ThreadFala = ''
        self.estado = Estado.LOGANDO
        self.run()

    
    def run(self):
        print("Insira o seu nome: ")
        self.nome = input()
        self.clienteRegistro = threading.Thread(target= self.clienteObj.iniciar_cliente, args=(self.nome, 'localhost', 5000)).start()
        #Posso receber convites
        self.estado = Estado.LIVRE
        #Thread que escuta convites
        self.ThreadEscuta = threading.Thread(target= self.escuta, args =(self.serverUDP))
        self.menu()


    def menu(self):
        time.sleep(10)
        self.clienteObj.libera_thread()
        dados = self.clienteObj.get_ultima_consulta()
        
        # Enquanto não convidei ninguém, verifico se convidei, ou se fui convidado 
        while dados == "":
            dados = self.clienteObj.get_ultima_consulta()


            # Se a thread que escuta mudou o estado
            while self.estado != Estado.LIVRE:
                pass
        
        mensagem = json.loads(dados)
        self.envia_convite(mensagem)

        
        

################################################################################################    # 
    
    def escuta(self, server):
        py_audio = py_audio.PyAudio()
        output_stream = py_audio.open(ac.SETTINGS)
        
        while True:
            mensagem = server.recvfrom(ac.BUFFER)
            mensagem = json.loads(mensagem)
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
                        server.sendto(json.dumps(mensagem), 'localhost', 6000)
                        enderecoContato = mensagem['dados']['ip']
                        portaContato = mensagem['dados']['porta']
                        self.ThreadFala = threading.Thread(target=self.servidor_envio, args=(enderecoContato, portaContato))
                        self.ThreadFala.start()

                    if resposta == 'n':
                        self.estado = Estado.LIVRE
                        mensagem = {"mensagem": "RECUSADO"}
                        server.sendto(json.dumps(mensagem), _address=(enderecoContato, portaContato))
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
                    server.send(json.dumps(mensagem))


################################################################################################################
        
    def servidor_envio(self, server, enderecoContato, portaContato):
        py_audio = pyaudio.PyAudio()
        input_stream = py_audio.open(ac.SETTINGS)
        while self.estado == Estado.OCUPADO:
            data = input_stream.read(ac.BUFFER, exception_on_overflow=False)
            mensagem = { "mensagem": "AUDIO", "dados": data}
            self.serverUDP.send(json.dumps(mensagem))
        mensagem = {"mensagem":"ENCERRAR_CHAMADA"}
        server.send(json.dumps(mensagem))

    
    def envia_convite(self, dados):
        self.estado = Estado.CONVIDANDO
        endereco = dados['ip']
        porta = dados['porta']
        
        self.serverUDP.bind(endereco, porta)
        mensagem = {
            'mensagem':'CONVITE',
            'dados': {
                'nome': self.nome,
                'IP': self.endereco,
                'port': self.porta 
            }
        }
        self.serverUDP.send(json.dumps(mensagem))

        
if __name__ == '__main__':
    app()
        

