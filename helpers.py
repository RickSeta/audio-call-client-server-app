import os


def mensagem_menu():
        print("Procure um usuário pelo nome")
        print("Para sair da aplicação, envie q")

def mensagem_convidado(self, usuario):
        print(usuario + " quer iniciar uma chamada")
        print("Para aceitar a chamada, envie s")
        print("Para recusar a chamada, envie n")

def mensagem_convidando():
        print("Aguarde a resposta do seu convite")


def mensagem_chamada(self, usuario):
        print("Sua chamada com " + usuario + "está em andamento")
        print("Para finalizar a chamada, envie q")         

def mensagem_recusado():
        print("Seu convite foi recusado")
        print("\n")
        texto_volte_ao_menu()

def mensagem_encerramento():
        print("Sua chamada foi finalizada")
        print("\n")
        texto_volte_ao_menu()

def texto_volte_ao_menu():
        print("Para retornar ao menu, envie q")

def mensagem_da_aplicacao(mensagem):
        print("Mensagem da aplicação: " + mensagem)