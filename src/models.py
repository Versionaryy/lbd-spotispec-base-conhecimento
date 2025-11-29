from pydantic import BaseModel

class Recomendacao(BaseModel):
    song: str
    artist: str
    spotify_url: str

class Regra(BaseModel):
    genero: str
    energia: str
    eh_curta: bool
    musicas: list[Recomendacao]


