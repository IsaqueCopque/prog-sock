import socket
import threading
from utils import formata_resposta

def start_server(PORT, N_SERVERS, MAX_N_CONN):
    """
    Inicia servidor proxy. Corpo de thread invocado por start_proxy em main.py.
    """
    HOST = socket.gethostbyname(socket.gethostname()) #Endereço ip local
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); #Cria socket IPV4 TCP
    sock.bind((HOST,PORT)) #Liga socket ao endereço ip com porta

    sock.listen()
    print("[PROXY] -> Escutando na porta ", PORT)

    while True:
        if (threading.active_count() - 2 - N_SERVERS) < MAX_N_CONN: #limita o número de conexões a MAX_N_CONN
                                                        # -2 threads = Thread main e thread Proxy
            connec, addr = sock.accept()
            thread = threading.Thread(target= handle_client, args=(connec, N_SERVERS, PORT, HOST))
            thread.start()
            print(f"[Proxy] -> TCP estabelecido com {addr}. Total de clientes ativos = ({threading.active_count() - 2 - N_SERVERS}).") 
        else: #Se ultrapassa limite, aceita conexão para apenas informar rejeição
            connec = sock.accept()[0]
            res = "[Proxy] -> Conexão rejeitada: Limite de conexões atingido."
            connec.send(res.encode('utf-8'))
            connec.close() #encerra conexão

def handle_client(connec, N_SERVERS, PORT, HOST):
    """
    Lida com as requisições do cliente. Corpo de thread.
    """
    try:
        resLength = connec.recv(1024).decode('utf-8')
        resLength = int(resLength)
        op = connec.recv(resLength).decode('utf-8') #recebe a operação
        op = op.split(" ") #[OP, FileName, FileSize, fLevel]
        op[2] = int(op[2])
        op[3] = int(op[3])
        if op[0] == "D": # Se depósito
            if op[3] > N_SERVERS or op[3]<0: #Se nível de tolerância maior que n servidores
                res, resLength = formata_resposta("[Proxy] -> Nível de tolerância não suportado")
                connec.send(resLength) #envia tamanho da resposta
                connec.send(res) #envia resposta
                connec.close()
            else: #Envia para os (fLevel) servidores o arquivo
                success = True
                data_received = 0
                serverSockets = []
                for i in range(op[3]):
                    sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sockServer.connect((HOST, PORT+i+1))
                    req, reqLength = formata_resposta(f"{op[0]} {op[1]} {op[2]}" )
                    sockServer.send(reqLength)          #envia tamanho da requisição
                    sockServer.send(req)                #envia requisição
                    serverSockets.append(sockServer)
                while op[2] > data_received:
                    bytes_read = connec.recv(1024)
                    if not bytes_read:
                        break
                    for sock in serverSockets:
                        sock.send(bytes_read)
                    data_received += 1024
                for sock in serverSockets:
                    resLength = sock.recv(1024).decode('utf-8')
                    res = sock.recv(int(resLength)).decode('utf-8')
                    decRes = res.split(':')[0]
                    if decRes == 'Sucesso':
                        success = True
                    else:
                        success = False
                    sock.close()
                if success: 
                    for i in range(op[3]+1, N_SERVERS+1):#atualiza numero de copias
                        sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sockServer.connect((HOST, PORT+i))
                        req, reqLength = formata_resposta(f"A {op[1]} 0")
                        sockServer.send(reqLength)          #envia tamanho da requisição
                        sockServer.send(req)                #envia requisição
                    res, resLength = formata_resposta("[Proxy] -> Sucesso ao depositar arquivo.")
                    connec.send(resLength)  #envia msg de sucesso para cliente       
                    connec.send(res)                
                connec.close()                          #encerra conexão cliente
        
        else: # Se recuperação op = [OP, FileName]
            found = False
            for i in range(1,N_SERVERS+1): #procura em todos servidores
                sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sockServer.connect((HOST,PORT+i))   #conecta ao servidor
                req, reqLength = formata_resposta( f"{op[0]} {op[1]} 0" )
                sockServer.send(reqLength)          #envia tamanho da requisição
                sockServer.send(req)                #envia requisição
                resLength = sockServer.recv(1024).decode('utf-8')   #recebe tamanho da resposta
                resLength = int(resLength)
                res = sockServer.recv(resLength)    #recebe resposta
                decRes = res.decode("utf-8")        #decodifica resposta
                decRes = decRes.split(":")             #separa resposta (Code: Msg)
                if decRes[0] == "Encontrado":       #Se encontrou (Encontrado: size)
                    found = True
                    filesize = int(decRes[1])
                    data_received = 0
                    res, resLength = formata_resposta(f"{decRes[0]}:{decRes[1]}")
                    connec.send(resLength)#envia tamanho para cliente
                    connec.send(res)
                    while filesize > data_received:
                        bytes_read = sockServer.recv(1024)
                        if not bytes_read:
                            break
                        connec.send(bytes_read)
                        data_received += 1024
                    sockServer.close()              #encerra conexão com servidor
                    break
                sockServer.close()              #encerra conexão com servidor
            if not found:                           #Se não encotrou arquivo -> -1
                res,resLength = formata_resposta("NaoEncontrado:-1")
                connec.send(resLength)  
                connec.send(res) 
            connec.close()                          #encerra conexão cliente                

    except Exception as e:
        print("[Proxy] -> Erro ao lidar com requisição. ", e.__class__)

    return None