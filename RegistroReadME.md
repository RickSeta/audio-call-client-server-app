Interações cliente servidor registro:

Servidor:
 basta chamar o arquivo com o python passando como argumentos ip e porta
ex: python3 ServidorRegistro.py localhost 5000

Cliente:

  crie um objeto ClienteRegistro.Cliente
  inicie uma thread passando nome de usuario,  ip e porta do servidor
  
  funções:
    get_ultima_consulta() retorna a resposta da ultima consulta feita
    libera_thread() destrava a thread do cliente fazendo com que um prompt de tipo de requisição seja feito
    
 exemplos no arquivo testing
    
