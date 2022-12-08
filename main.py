import threading
import proxy
import server

# Variáveis Globais
N_SERVERS = 5       #quantidade de servidores locais
MAX_N_CONN = 3      #quantidade máxima de clientes conectados ao servidor proxy
PORT_PROXY = 60000  #porta para o servidor proxy
HEADER = 1024         #tamanho da primeira mensagem
# ------

# ---Funções---

def start_servers():
    """
    Inicia os servidores locais.
    """
    for i in range(N_SERVERS):
        print(f"-> Iniciando servidor {i+1} na porta {PORT_PROXY+i+1}.")
        serverThread = threading.Thread(target = server.start_server, args=(PORT_PROXY+i+1,))
        serverThread.start() 
    print(f"-> {N_SERVERS} servidores iniciados.")

def start_proxy():
    """
    Inicia servidor proxy.
    """
    print("-> Iniciando servidor Proxy.")
    proxyThread = threading.Thread(
        target = proxy.start_server, 
        args=(
            PORT_PROXY,
            N_SERVERS,
            MAX_N_CONN,
            HEADER,
            )
    )
    proxyThread.start()
    print("-> Servidor Proxy iniciado.")

#---Main---
start_proxy()
start_servers()