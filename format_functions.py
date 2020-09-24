from settings import DICIONARIO

def format_municipio(el):
    try:
        return DICIONARIO['id_municipio'][el]
    except:
        return 'Não encontrado'

def format_uf(el):
    return DICIONARIO['id_uf'][str(el)]

def format_serie(el):
    return DICIONARIO['id_serie'][el]
