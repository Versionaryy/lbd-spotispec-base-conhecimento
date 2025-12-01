from pydantic import BaseModel

class Recomendacao(BaseModel):
    titulo: str
    artista: str
    spotify_url: str 

class Regra(BaseModel):
    genero: str
    energia: str
    eh_curta: bool
    musicas: list[Recomendacao]


