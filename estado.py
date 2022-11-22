import enum

class Estado(enum):
    LOGANDO = -1
    LIVRE = 0
    CONVIDANDO = 1
    CONVIDADO = 2
    OCUPADO = 3