import socket
from os import makedirs
from os.path import getsize, normpath, exists
from utils import check_file, formata_resposta

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000
USR_FOLDER = "local"
# ---

def get_input():
    """
    Obtém do cliente a operação a ser realizada e o nome de arquivo.
    Retorna Operação, Nome de Arquivo, Nível de Tolerância
    """
    while True:
        op = input("Informe a operação a ser realizada (D) Depósito (R) Recuperação (E) Encerrar: ")
        op = op.upper()
        nomeOp = "armazenado" if op == "D" else "recuperado"
        if op == 'D' or op == 'R':
            arq = input(f"Informe o arquivo a ser {nomeOp}: ")
            if (op == 'D') and not check_file(arq): #Arquivo inválido
                print("Arquivo inválido")
                continue
            fLevel = None
            if op == 'D':
                fLevel = input("Informe o nível de tolerância a falhas: ")
            return op,arq,fLevel
        if op == 'E':
            return op, None, None

def send_file_to_server(arq, sock):
    with open(arq, "rb") as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            sock.send(bytes_read)

def get_file_from_server(arq):
    resLength = sock.recv(1024).decode('utf-8')
    resLength = int(resLength)
    res = sock.recv(resLength).decode('utf-8')
    found = res.split(":")
    filesize = int(found[1])
    if found[0] == "Encontrado":
        if not exists(USR_FOLDER):
            makedirs(USR_FOLDER)
        filepath = f"{USR_FOLDER}/{arq}"
        if exists(filepath):
            filename = normpath(filepath)
        else:
            filename = normpath(filepath)
        data_received = 0
        with open(filename, "wb") as f:
            while filesize > data_received:
                bytes_read = sock.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
                data_received += 1024
        print("Arquivo recuperado")
    else:
        print("Arquivo não encontrado.")

try:                     
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST,PORT))
        op, arq, fLevel = get_input()
        if op == 'D': #Depósito
            arqSize = getsize(arq) #tamanho do arquivo a ser enviado
            req, reqlength = formata_resposta(f"D {arq} {arqSize} {fLevel}")
            sock.send(reqlength)
            sock.send(req)
            send_file_to_server(arq, sock)
            resLength = sock.recv(1024).decode('utf-8')
            res = sock.recv(int(resLength))
            print(res.decode('utf-8'))
        elif op == 'R': #Recuperação
            req, reqlength = formata_resposta(f"R {arq} 0 0")
            sock.send(reqlength)
            sock.send(req)
            get_file_from_server(arq)
        else:
            break
except Exception as e:
    print("-> Erro ao criar conexão com servidor.", e.__class__)