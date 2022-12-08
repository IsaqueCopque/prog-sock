import socket
from os.path import exists, getsize

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000
HEADER = 64

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ---

def check_file(arq):
    """
    Verifica se o arquivo informado pelo cliente é válido e existe.
    """
    dotIndex = arq.find('.')
    if dotIndex != -1:
        finalP = len(arq)-1
        if finalP-dotIndex > 0: #possui extensao depois do '.'
            return exists(arq)
    else:
        return False

def get_input():
    """
    Obtém do cliente a operação a ser realizada e o nome de arquivo.
    Retorna Operação, Nome de Arquivo, Nível de Tolerância
    """
    while True:
        op = input("Informe a operação a ser realizada: (D) Depósito (R) Recuperação")
        if op == 'D' or op == 'd' or op == 'R' or op == 'r':
            arq = input("Informe o arquivo a ser armazenado: ")
            if not check_file(arq): #Arquivo inválido
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
        arqSize = getsize(arq) #tamanho do arquivo a ser enviado
        if op == 'D' or op == 'd': #Depósito
            send_file_to_server(arq, fLevel)
            #send_to_server("Mensagem DEPOSITO") #POR ENQUANTO SÓ MANDA MENSAGEM
        else: #Recuperação
            send_to_server("Mensagem RECUPERACAO") #POR ENQUANTO SÓ MANDA MENSAGEM
    except Exception as e:
        print("-> Erro ao criar conexão com servidor.", e.__class__)

def send_file_to_server(arq, fLevel):
    arqSize = getsize(arq) #tamanho do arquivo a ser enviado
    encData = f"{arq}{SEPARATOR}{arqSize}{SEPARATOR}{fLevel}".encode('utf-8')
    sock.send(encData)
    with open(arq, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            sock.send(bytes_read)
    res = sock.recv(1024).decode('utf-8')
    print(res)

def send_to_server(data):
    """
    Envia dados ao servidor. POR ENQUANTO SÓ MANDA MENSAGEM
    """
    encData = data.encode('utf-8')
    sock.send(encData)
    #TESTA RESPOSTA
    res = sock.recv(1024).decode('utf-8')
    print(res)

connect_to_server()