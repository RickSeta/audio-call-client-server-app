Interações cliente servidor registro:

      Servidor: basta chamar o arquivo com o python passando como argumentos ip e porta 
      ex: python3 ServidorRegistro.py localhost 5000

      Cliente:

         crie um objeto ClienteRegistro.Cliente inicie uma thread passando nome de usuario, ip e porta do servidor

         funções: 
            get_ultima_consulta() retorna a resposta da ultima consulta feita
            libera_thread(): destrava a thread do cliente fazendo com que um prompt de tipo de requisição seja feito

         exemplos uso cliente no arquivo testing


![image](https://user-images.githubusercontent.com/54965077/200019962-05523315-84c3-460c-a34b-20f5a7cc36c6.png)
![image](https://user-images.githubusercontent.com/54965077/200020008-c8be53f7-f7ec-4319-b178-647d5b2b984e.png)
![image](https://user-images.githubusercontent.com/54965077/200020054-41458aa0-0834-43bc-a74b-e9db6b117a6b.png)
![image](https://user-images.githubusercontent.com/54965077/200020098-4d0e77fb-fd55-4749-bf1f-1022a5a4b5c1.png)

Links:

https://realpython.com/python-sockets/#socket-api-overview 

https://pythontic.com/modules/socket/udp-client-server-example 

https://www.cs.dartmouth.edu/~campbell/cs60/socketprogramming.html 

https://pypi.org/project/PyAudio/ 

