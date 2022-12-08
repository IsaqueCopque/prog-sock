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