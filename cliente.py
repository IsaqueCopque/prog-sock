import socket
from os.path import getsize
from utils import check_file, formata_resposta

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ---

def get_input():
    """
    Obtém do cliente a operação a ser realizada e o nome de arquivo.
    Retorna Operação, Nome de Arquivo, Nível de Tolerância
    """
    while True:
        op = input("Informe a operação a ser realizada: (D) Depósito (R) Recuperação\n")
        if op == 'D' or op == 'd' or op == 'R' or op == 'r':
            arq = input("Informe o arquivo a ser armazenado: ")
            if not check_file(arq): #Arquivo inválido
                print("Arquivo inválido")
                continue
            fLevel = None
            if op == 'D' or op == 'd':
                fLevel = input("Informe o nível de tolerância a falhas: ")
            return op,arq,fLevel

def send_file_to_server(arq, sock):
    with open(arq, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            sock.send(bytes_read)

try:                     
    sock.connect((HOST,PORT))
    while True:
        op, arq, fLevel = get_input()
        arqSize = getsize(arq) #tamanho do arquivo a ser enviado
        if op == 'D' or op == 'd': #Depósito
            req, reqlength = formata_resposta(f"D {arq} {arqSize} {fLevel}")
            sock.send(reqlength)
            sock.send(req)
            resLength = sock.recv(1024)
            send_file_to_server(arq, sock)
            res = sock.recv(resLength)
            print(res.decode())
        else: #Recuperação
            req, reqlength = formata_resposta(f"R {arq}")
            sock.send(reqlength)
            sock.send(req)
            resLength = sock.recv(1024)
            res = sock.recv(resLength)
            print(res.decode())
except Exception as e:
    print("-> Erro ao criar conexão com servidor.", e.__class__)