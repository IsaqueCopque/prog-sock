import socket
import threading
from os.path import normpath, getsize
from utils import check_file

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000
MAX_N_CONN = 3 #quantidade maxima de clientes conectados ao servidor
HEADER = 64 #tamanho da primeira mensagem

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# ---

def save_file(connec, filename, filesize):
    filename = normpath(f"files/{filename}")
    filesize = int(filesize)
    data_received = 0
    with open(filename, "wb") as f:
        while filesize > data_received:
            bytes_read = connec.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            data_received += BUFFER_SIZE

def get_file(connec, filename):
    if not check_file(f"files/{filename}"):
        connec.send(f"False{SEPARATOR}0".encode('utf-8'))
    else: 
        filesize = getsize(f"files/{filename}")
        connec.send(f"True{SEPARATOR}{filesize}".encode('utf-8'))
        with open(f"files/{filename}", "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                connec.sendall(bytes_read)

def handle_client(connec,addr):
    """
    Lida com as requisições do cliente. Corpo de thread.
    """
    data = connec.recv(1024).decode('utf-8')
    op, filename, filesize, fLevel = data.split(SEPARATOR)
    if op == 'd':
        print(f"-> Recebido de {addr}: {filename} com tamanho {filesize} bytes com nível de tolerância {fLevel}\n")
        save_file(connec, filename, filesize)
    if op == 'r':
        print(f"Recebido de {addr}: baixar {filename}\n")
        get_file(connec, filename)
    resposta = "Servidor diz: MSG recebida, encerrando conexão"
    resposta = resposta.encode('utf-8')
    connec.send(resposta)
    
    # isconn = True
    # while isconn:
    #     data_length = connec.recv(HEADER).decode('utf-8') #recebe o tamanho do arquivo a ser recebido
    #     if data_length:
    #         data_length = int(data_length)
    #         data = connec.recv(data_length)
    #         if data == "disc":
    #             isconn= False
    connec.close()

def start_server():
    """
    Inicia o servidor. Servidor aceita novas conexões enquanto N_CONN < MAX_N_CONN.
    """
    sock.listen()
    print("-> Servidor escutando na porta", PORT)
    while True:
        if (threading.active_count() - 1) < MAX_N_CONN: #limita o número de conexões a MAX_N_CONN
            connec, addr = sock.accept()
            thread = threading.Thread(target= handle_client, args=(connec,addr))
            thread.start()
            print(f"-> TCP estabelecido com {addr}. Total de clientes = ({threading.active_count() - 1}).")
    
sock.bind((HOST,PORT))
start_server()