import socket
from os.path import exists, getsize, normpath
from utils import check_file

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000
HEADER = 64

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ---

def get_input():
    """
    Obtém do cliente a operação a ser realizada e o nome de arquivo.
    Retorna Operação, Nome de Arquivo, Nível de Tolerância
    """
    while True:
        op = input("Informe a operação a ser realizada: (D) Depósito (R) Recuperação")
        if op == 'D' or op == 'd' or op == 'R' or op == 'r':
            arq = input("Informe o arquivo a ser armazenado: ")
            if (op == 'D' or op == 'd') and not check_file(arq): #Arquivo inválido
                print("Arquivo inválido")
                continue
            fLevel = None
            if op == 'D' or op == 'd':
                fLevel = input("Informe o nível de tolerância a falhas: ")
            return op,arq,fLevel
                             
def connect_to_server():
    try:
        sock.connect((HOST,PORT))
        op, arq, fLevel = get_input()
        #arqSize = getsize(arq) #tamanho do arquivo a ser enviado
        if op == 'D' or op == 'd': #Depósito
            send_file_to_server(arq, fLevel)
            #send_to_server("Mensagem DEPOSITO") #POR ENQUANTO SÓ MANDA MENSAGEM
        else: #Recuperação
            get_file_from_server(arq)
            #send_to_server("Mensagem RECUPERACAO") #POR ENQUANTO SÓ MANDA MENSAGEM
    except Exception as e:
        print("-> Erro ao criar conexão com servidor.", e.__class__)

def send_file_to_server(arq, fLevel):
    arqSize = getsize(arq) #tamanho do arquivo a ser enviado
    encData = f"d{SEPARATOR}{arq}{SEPARATOR}{arqSize}{SEPARATOR}{fLevel}".encode('utf-8')
    sock.send(encData)
    with open(arq, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            sock.sendall(bytes_read)
    res = sock.recv(1024).decode('utf-8')
    print(res)

def get_file_from_server(arq):
    encData = f"r{SEPARATOR}{arq}{SEPARATOR}0{SEPARATOR}0".encode('utf-8')
    sock.send(encData)
    found, filesize = sock.recv(1024).decode('utf-8').split(SEPARATOR)
    filesize = int(filesize)
    filename = normpath(arq)
    print(f"Arquivo com tamanho {filesize} bytes\n")
    if bool(found):
        data_received = 0
        with open(filename, "wb") as f:
            while filesize > data_received:
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                data_received += BUFFER_SIZE
    res = sock.recv(1024).decode('utf-8')
    print(res)

connect_to_server()