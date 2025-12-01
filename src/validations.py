import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import boto3
from boto3.dynamodb.conditions import Key


load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)



aws_region = os.getenv("AWS_REGION")
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table('SpotispecKnowledgeBase')

def validar_musica_duplicada(genero, energia, eh_curta, url):
    chave = f'{genero}#{energia}#{str(eh_curta).lower()}'
    query_recomendacao = table.query(
        KeyConditionExpression=Key('SE_KEY').eq(chave)
    )
    items = query_recomendacao.get('Items', [])
    for item in items:
        musicas = item.get('musicas', [])
        for m in musicas:
            if m.get('spotify_url') == url:
                return 'Música com essa URL já existe para essa regra', False
    return '', True


def validar_duracao(url, eh_curta):
    erros = []
    musica = sp.track(url)


    duracao = musica.get('duration_ms')

    if duracao > 210000 and eh_curta is True:
        return 'Música não é curta', False
    elif duracao < 210000 and eh_curta is False:
        return 'Música é curta', False
    return '', True

def validar_musica(genero, energia, eh_curta, url):
    '''
    validar regra
    - gênero válido
    - energia válida
    - valor de eh_curta como true ou false
    
    Retorna tupla (lista_de_erros, sucesso)
    '''
    LISTA_GENEROS = [
        'Pop',
        'Rock',
        'Sertanejo',
        'Metal',
        'Hip-Hop'
    ]
    LISTA_ENERGIAS = [
        'Alta',
        'Media',
        'Baixa'
    ]
    
    erros = []
    
    if genero not in LISTA_GENEROS:
        erros.append('Gênero inválido')
    
    if energia not in LISTA_ENERGIAS:
        erros.append('Energia inválida')
    
    if eh_curta is not True and eh_curta is not False:
        erros.append('Não foi possível identificar se deve ser curta ou não')
    
    (mensagem, sucesso_duracao) = validar_duracao(url, eh_curta)
    if not sucesso_duracao:
        erros.append(mensagem)

    (mensagem_dup, sucesso_dup) = validar_musica_duplicada(genero, energia, eh_curta, url)
    if not sucesso_dup:
        erros.append(mensagem_dup)

    sucesso = len(erros) == 0
    return erros, sucesso
    