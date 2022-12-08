import socket
import threading

def start_server(PORT, N_SERVERS, MAX_N_CONN, HEADER):
    """
    Inicia servidor proxy. Corpo de thread invocado por start_proxy em main.py.
    """
    HOST = socket.gethostbyname(socket.gethostname()) #Endereço ip local
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); #Cria socket IPV4 TCP
    sock.bind((HOST,PORT)) #Liga socket ao endereço ip com porta

    sock.listen()
    print("[PROXY] -> Escutando na porta ", PORT)

    while True:
        if (threading.active_count() - 2) < MAX_N_CONN: #limita o número de conexões a MAX_N_CONN
                                                        # -2 threads = Thread main e thread Proxy
            connec, addr = sock.accept()
            thread = threading.Thread(target= handle_client, args=(connec,addr, HEADER, N_SERVERS, PORT, HOST))
            thread.start()
            print(f"[Proxy] -> TCP estabelecido com {addr}. Total de clientes ativos = ({threading.active_count() - 2}).") 
        else: #Se ultrapassa limite, aceita conexão para apenas informar rejeição
            connec = sock.accept() 
            res = "[Proxy] -> Conexão rejeitada: Limite de conexões atingido."
            connec.send(res.encode('utf-8'))
            connec.close() #encerra conexão

def handle_client(connec,addr, HEADER, N_SERVERS, PORT, HOST):
    """
    Lida com as requisições do cliente. Corpo de thread.
    """
    try:
        op = connec.recv(HEADER).decode('utf-8') #recebe a operação
        op = op.split(" ") #[OP, FileName, FileSize, fLevel]
        op[2] = int(op[2])
        op[3] = int(op[3])

        if op[0] == "D": # Se depósito
            if op[3] > N_SERVERS or op[3]<=0: #Se nível de tolerância maior que n servidores
                res, resLength = formata_resposta("[Proxy] -> Nível de tolerância não suportado")
                connec.send(resLength) #envia tamanho da resposta
                connec.send(res) #envia resposta
                connec.close()
            else: #Envia para os (fLevel) servidores o arquivo
                file = connec.recv(op[2]) #recebe o arquivo
                #........ ver como recebe
                sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                success = True
                for i in range(1,op[3]+1): #Envia para cada (fLevel) servidores
                    sockServer.connect((HOST,PORT+i))   #conecta ao servidor
                    req, reqLength = formata_resposta( f"{op[0]} {op[1]} {op[2]}".encode("uft-8") )
                    sockServer.send(reqLength)          #envia tamanho da requisição
                    sockServer.send(req)                #envia requisição
                    sockServer.send(file)               #envia arquivo
                    resLength = sockServer.recv(1024)   #recebe tamanho da resposta
                    res = sockServer.recv(resLength)    #recebe resposta
                    decRes = res.decode("utf-8")        #decodifica resposta
                    decRes = res.split(":")             #separa resposta (Code: Msg)
                    if decRes[0] != "Sucesso":          #se falhou para algum servidor
                        connec.send(resLength)          #tamanho msg para cliente
                        connec.send(res)                #msg de falha para cliente
                        sockServer.close()              #encerra conexão com servidor
                        success = False
                        break
                    sockServer.close()                  #encerra conexão com servidor
                if success:                             #msg de sucesso para cliente
                    res, resLength = formata_resposta("[Proxy] -> Sucesso ao depositar arquivo.")
                    connec.send(resLength)         
                    connec.send(res)                
                connec.close()                          #encerra conexão cliente
        
        else: # Se recuperação op = [OP, FileName]
            sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            found = False
            for i in range(1,N_SERVERS+1): #procura em todos servidores
                sockServer.connect((HOST,PORT+i))   #conecta ao servidor
                req, reqLength = formata_resposta( f"{op[0]} {op[1]}".encode("uft-8") )
                sockServer.send(reqLength)          #envia tamanho da requisição
                sockServer.send(req)                #envia requisição
                resLength = sockServer.recv(1024)   #recebe tamanho da resposta
                res = sockServer.recv(resLength)    #recebe resposta
                decRes = res.decode("utf-8")        #decodifica resposta
                decRes = res.split(":")             #separa resposta (Code: Msg)
                if decRes[0] == "Encontrado":       #Se encontrou (Encontrado: size)
                    found = True
                    res = sockServer.recv(int(decRes[1]))
                    connec.send(int(decRes[1]))     #envia tamanho para cliente
                    connec.send(res)                #envia arquivo para cliente
                    sockServer.close()              #encerra conexão com servidor
                    break
            sockServer.close()                  #encerra conexão com servidor
            if not found:                           #Se não encotrou arquivo -> -1
                res,resLength = formata_resposta("-1")
                connec.send(resLength)         
                connec.send(res) 
            connec.close()                          #encerra conexão cliente                

    except Exception as e:
        print("[Proxy] -> Erro ao lidar com requisição. ", e.__class__)

    return None

def formata_resposta(res):
    """
    Formata a resposta, devolve mensagem formatada e seu tamanho. 
    """
    resMsg = res.encode('utf-8')
    msgLength = len(resMsg)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (1024 - len(sendLength))
    return resMsg, sendLength