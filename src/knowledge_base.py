'''
Código com os módulos de Aquisição de Conhecimento e Base de Conhecimento
'''

from src.models import Recomendacao
import boto3
from boto3.dynamodb.conditions import Key
from .validations import validar_musica
import os
from dotenv import load_dotenv
load_dotenv()

aws_region = os.environ.get("AWS_REGION")
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table('SpotispecKnowledgeBase')

def atualizar_regra(genero, energia, eh_curta, musica):
    '''
    se tem: altera a regra pra adicionar (update_item) 
    
    '''
    chave = f'{genero}#{energia}#{str(eh_curta).lower()}'
    novo_item = {
        'titulo': musica.titulo,
        'artista': musica.artista,
        'spotify_url': musica.spotify_url
    }
    try:
        resp = table.update_item(
            Key={'SE_KEY': chave},
            UpdateExpression='SET musicas = list_append(if_not_exists(musicas, :empty_list), :new_items)',
            ExpressionAttributeValues={
                ':new_items': [novo_item],
                ':empty_list': []
            },
            ReturnValues='UPDATED_NEW'
        )
        print('Regra atualizada:', resp)
        return True, resp
    except Exception as e:
        print('Erro ao atualizar regra:', e)
        return False, str(e)

def adicionar_regra(genero, energia, eh_curta, musica):
    '''
    se não tem: nova regra (put_item)
    '''
    chave = f'{genero}#{energia}#{str(eh_curta).lower()}'
    item = {
        'SE_KEY': chave,
        'musicas': [
            {
                'titulo': musica.titulo,
                'artista': musica.artista,
                'spotify_url': musica.spotify_url
            }
        ]
    }
    try:
        resp = table.put_item(Item=item)
        print('Regra adicionada:', resp)
        return True, resp
    except Exception as e:
        print('Erro ao adicionar regra:', e)
        return False, str(e)

def adquirir_conhecimento(genero: str, energia: str, eh_curta: bool, musica: Recomendacao) -> tuple:
    caracteristicas_musica = (genero, energia, eh_curta)
    (erros_regra, sucesso_regra) = validar_musica(genero, energia, eh_curta, musica.spotify_url)

    if not sucesso_regra:
        return False, {"erros": erros_regra}
    
    chave = f'{genero}#{energia}#{str(eh_curta).lower()}'
    query_recomendacao = table.query(
        KeyConditionExpression=Key('SE_KEY').eq(chave)
    )

    count = query_recomendacao.get('Count', 0)
    if count > 0:
        atualizar_regra(genero, energia, eh_curta, musica)
    else:
        adicionar_regra(genero, energia, eh_curta, musica)

    return True, f"Música '{musica.titulo}' adicionada com sucesso"
    
