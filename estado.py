from enum import Enum

class Estado(Enum):
    LOGANDO = -1
    LIVRE = 0
    CONVIDANDO = 1
    CONVIDADO = 2
    OCUPADO = 3