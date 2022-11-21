import os


def limpa_tela():
        os.system('cls')

def tela_menu():
        limpa_tela()
        print("Procure um usuário pelo nome")
        print("Para sair da aplicação, envie q")

def tela_convidado(self, usuario):
        limpa_tela()
        print(usuario + " quer iniciar uma chamada")
        print("Para aceitar a chamada, envie s")
        print("Para recusar a chamada, envie n")

def tela_convidando():
        limpa_tela()
        print("Aguarde a resposta do seu convite")


def tela_chamada(self, usuario):
        limpa_tela()
        print("Sua chamada com " + usuario + "está em andamento")
        print("Para finalizar a chamada, envie q")         

def tela_recusado():
        limpa_tela()
        print("Seu convite foi recusado")
        print("\n")
        texto_volte_ao_menu()

def tela_encerramento():
        print("Sua chamada foi finalizada")
        print("\n")
        texto_volte_ao_menu()

def texto_volte_ao_menu():
        print("Para retornar ao menu, envie q")

def mensagem_da_aplicacao(mensagem):
        print("Mensagem da aplicação: " + mensagem)