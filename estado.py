import enum

class Estado(enum):
    LIVRE = 0
    CONVIDANDO = 1
    CONVIDADO = 2
    OCUPADO = 3

# class EstadoDoCliente:
#     estado = Estado

#     def __init__(self):
#         self.estado = Estado.LIVRE

#     def get_estado(self):
#         return self.estado

#     def set_estado(self, novo_estado):
#         self.estado = novo_estado
