import json
import threading


class Pacote:
    
    def __init__(self, sock, endereco="", listaRegistros ={}):
        self.sock = sock
        self.nome = ""
        self.endereco = endereco
        self._recv_buffer = b""
        self._send_buffer = b""
        self.tipo_req = b""
        self.jsonheader = None
        self.listaReg = listaRegistros

    def _read(self, tamanho=4096):
        try:
            data = self.sock.recv(tamanho)
        except BlockingIOError:
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                self.encerra_conexao(self.nome)
                print('ata')
                raise RuntimeError("Peer fechado")

    def _read_byte(self):
        try:
            data = self.sock.recv(1)
        except BlockingIOError:
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer fechado")

    def _write(self):
        if self._send_buffer:
            print(f"Enviando {self._send_buffer!r} para {self.endereco}")
            try:
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Fecha quando ja tiver enviado tudo.
                if sent and not self._send_buffer:
                    print("Fim do envio")

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = json_bytes.decode(encoding)
        print(tiow)
        obj = json.loads(tiow)

        return obj

    def close(self):
        print(f"Fechando conexao com {self.endereco}")

        try:
            self.sock.close()
            print("Fechado!")
        except OSError as e:
            print(f"Erro: socket.close() exception para {self.endereco}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def processar_recebimento(self):
        aberto = True
        while aberto:
            self._read()
            if self._recv_buffer:
                content = self._json_decode(
                    self._recv_buffer, "utf-8"
                )
                self._recv_buffer = b""

                tipo_pedido = content["tipo-pedido"]
                if tipo_pedido == "c":
                    print(content)
                    print('consulta')
                    self.consulta_lista(content['consulta'])
                elif tipo_pedido == "r":
                    print('registro')
                    self._registra_lista(content['nome'])
                elif tipo_pedido == 'f':
                    aberto = False
                    self.encerra_conexao(content['nome'])
                else:
                    raise ValueError(f"Seguinte tipo nao valido: '{tipo_pedido}'.")


    def _registra_lista(self, nome):
        if nome not in self.listaReg:
            self.listaReg[nome] = {"ip": self.endereco[0], "porta": self.endereco[1]}
            print(self.listaReg)
            self.nome = nome
            #self._send_buffer = self._json_encode(self.listaReg, "utf-8")
            self._send_buffer = b'Usuario registrado!'
            self._write()
        else:
            print("Por favor escolha outro nome")
            self._send_buffer = b'Por favor escolha outro nome'
            self._write()
            self.close()
            print(self.listaReg)

    def consulta_lista(self, nome):
        if nome in self.listaReg:
            self._send_buffer = self._json_encode(self.listaReg[nome], "utf-8")
            print()
        else:
            self._send_buffer = b"Pessoa nao encontrada"

        self._write()

    def encerra_conexao(self, nome):
        self._send_buffer = b'Encerrando conexao!'
        del self.listaReg[nome]
        self._write()
        self.close()


