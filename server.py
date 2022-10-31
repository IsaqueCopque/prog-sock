import socket
import threading

# Variáveis Globais
HOST = socket.gethostbyname(socket.gethostname())
PORT = 60000
MAX_N_CONN = 3 #quantidade maxima de clientes conectados ao servidor
HEADER = 64 #tamanho da primeira mensagem

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# ---

def handle_client(connec,addr):
    """
    Lida com as requisições do cliente. Corpo de thread.
    """
    data = connec.recv(1024).decode('utf-8')
    print(f"-> Recebido de {addr}: {data}")
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