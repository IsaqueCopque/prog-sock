from os.path import exists

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

def formata_resposta(res):
    """
    Formata a resposta, devolve mensagem formatada e seu tamanho. 
    """
    resMsg = res.encode('utf-8')
    msgLength = len(resMsg)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (1024 - len(sendLength))
    return resMsg, sendLength