# Chat
É um projeto feito em [python](https://www.python.org/) utilizando o framework [flask](http://flask.pocoo.org/) e [MongoDB](https://www.mongodb.com/) visando a construção de um chat fazendo uso de uma api rest e uma aplicação web.

> Este projeto foi divido em duas aplicações:
> Uma cria um app rest que por sua vez fornece
> acesso ao banco de dados mongo de maneira simples.
> Enquanto a outra executa uma aplicação web que
> faz requisições a api rest para consumi-la.

### Preparando o ambiente

Para que o ambiente seja preparado de maneira correta, basta executar o comando abaixo:
```
sudo configure.sh
```

### Executando os testes
```
run_tests.sh
```
### Executando a api rest
```
run_web_app.sh
```
### Executando o web app
```
run_web_app.sh
```

### Como proceder o acesso ao chat
Após a execução da aplicação rest e da aplicação web basta navegar no endereço abaixo, seguido do nome da sala:
```
http://localhost:8000/<room_name>
```