import socket
import os
from os.path import normpath, getsize
from utils import check_file, formata_resposta

# Variáveis Globais
BUFFER_SIZE = 1024
SEPARATOR = " "
# ---

def save_file(connec, filename, filesize, foldername):
    filename = normpath(f"{foldername}/{filename}")
    filesize = int(filesize)
    data_received = 0
    with open(filename, "wb") as f:
        while filesize > data_received:
            bytes_read = connec.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            data_received += BUFFER_SIZE

def get_file(connec, filename, foldername):
    if not check_file(f"{foldername}/{filename}"): #não encotrado
        res,resLength = formata_resposta("NaoEncontrado:")
        connec.send(resLength) #retorna tamanho da resposta
        connec.send(res) #retorna a resposta
    else: 
        filesize = getsize(f"{foldername}/{filename}")
        res,resLength = formata_resposta(f"Encontrado:{filesize}")
        connec.send(resLength) #retorna tamanho da resposta
        connec.send(res) #retorna a resposta
        with open(f"{foldername}/{filename}", "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                connec.sendall(bytes_read)

def delete_file(filename, foldername):
    if check_file(f"{foldername}/{filename}"):
        os.remove(f"{foldername}/{filename}")

def start_server(PORT):
    """
    Inicia o servidor.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.listen()
    print("-> Servidor escutando na porta", PORT)
    while True:
        connec = sock.accept()
        data = connec.recv(1024).decode('utf-8')
        op, filename, filesize = data.split(SEPARATOR)

        if op == 'D': #Depositar
            print(f"[{PORT}]-> Recebido: {filename} com tamanho {filesize} bytes.\n")
            try:
                save_file(connec, filename, filesize, PORT)
                res,resLength = formata_resposta("Sucesso:")
                connec.send(resLength) #retorna tamanho da resposta
                connec.send(res) #retorna a resposta
            except Exception as e: #Erro ao salvar arquivo
                res,resLength = formata_resposta("Falha:"+e)
                connec.send(resLength) #retorna tamanho da resposta
                connec.send(res) #retorna a resposta

        if op == "R":# Recuperar
            print(f"[{PORT}]Recebido: Recuperar {filename}\n")
            get_file(connec, filename, PORT)

        if op == 'A': #Deletar
            print(f"[{PORT}]Recebido: Deletar {filename}\n")
            delete_file(connec,filename, PORT)