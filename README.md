# Trabalho de sockets - Redes de Computadores - MATA 59

Alunos: Isaque Copque(219120256), João Pedro Fernandes(219217088), Matheus Novais(219115204), Matheus Guimarães(219116051)

Professor: Gustavo Bittencourt Figueiredo

---

## Requisitos

Este projeto foi criado para o trabalho de sockets de Redes de Computadores. Para rodar o projeto é necessário ter a linguagem [Python](https://www.python.org) instalada, este projeto também utiliza threads para executar os servidores.

---
## Objetivo
A aplicação segue o modelo cliente-servidor. Através dela o usuário consegue depositar arquivos com replicação e recuperar esses arquivos utilizando os modos de depósito e recuperação.

Para iniciar a aplicação, deve-se entrar na pasta do projeto e executar o comando:

``` bash
python main.py

```
ou

```bash
python3 main.py
```

Este comando irá iniciar todos os servidores inclusive o servidor de proxy .

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
### Modo de Depósito

Para realizar um depósito você precisa ter o arquivo na pasta raiz do projeto, então quando for solicitada a entrada do arquivo para ser depositado, você precisa passar o nome do arquivo com sua extensão.
Então será solicitado o nível de tolerância a falhas do arquivo, ele representa a quantidade de dispositivos em que ficarão salvas as cópias do documento. Para salvar os arquivos, a aplicação cria, para cada servidor, uma pasta server com a porta do servidores como nome, e nelas armazena as cópias dos arquivos.

### Modo de Recuperação

Para recuperar um arquivo, ao escolher a opção de recuperação, a aplicação solicitará que você digite o nome do arquivo a ser recuperado, caso ele seja encontrado em um dos servidores existentes, a aplicação criará uma pasta local e colocará os arquivos recuperados nela, caso não seja econtrado será informada a não existência do arquivo.
