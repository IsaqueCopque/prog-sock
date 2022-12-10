# Trabalho de sockets - Redes de Computadores - MATA 59

Alunos: Isaque Copque(219120256), João Pedro Fernandes(219217088), Matheus Novais(219115204), Matheus Guimarães()

Professor: Gustavo Bittencourt Figueiredo

---

## Requisitos

Este projeto foi criado para o trabalho de sockets de Redes de Computadores. Para rodar o projeto é necessário ter a linguagem [Python](https://www.python.org) instalada.

---
## Objetivo
A aplicação segue o modelo cliente-servidor. Através dela o usuário consegue depositar arquivos com replicação e recuperar esses arquivos utilizando os dois modos de depósito e recuperação.

Para iniciar a aplicação deve-se entrar na pasta do projeto e executar o comando:

``` bash
python main.py

```
ou

```bash
python3 main.py
```

Este comando irá iniciar todos os servidores inclusive o servidor de proxy.

Agora, que os servidores estão rodando, você poderá utilizar as funcionalidades da aplicação de depósito ou recuperação de arquivos.

Para utilizar essas funcionalidades você precisará iniciar outro terminal como cliente utilizando o comando:

``` bash
python cliente.py

```
ou

```bash
python3 cliente.py
```
Então você deve escolher D para depósito ou R para recuperação.
### Modo de depósito

Para realizar um depósito você precisa ter o arquivo na pasta raiz do projeto
 