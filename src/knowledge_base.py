'''
Código com os módulos de Aquisição de Conhecimento e Base de Conhecimento
'''


# base de conecimento
# cada música tem: gênero, energia e se é curta ou não

from src.models import Recomendacao


KNOWLEDGE_BASE = {
    ("Pop", "Alta", True): [{"song": "Prisioner", "artist": "Miley Cyrus", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}, {"song": "Espresso", "artist": "Sabrina Carpenter", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"},  {"song":"Rain On Me", "artist": "Lady Gaga", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}],
    ("Rock", "Baixa", False): [{"song":"Wish You Were Here","artist":  "Pink Floyd", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}, {"song":"Changes", "artist": "Black Sabbath", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}],
    ("Hip Hop", "Baixa", True): [{"song": "Under The Influence", "artist": "Chris Brown", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}, { "song":"So Sick", "artist": "Ne-Yo", "url": "https://open.spotify.com/intl-pt/track/4eHbdreAnSOrDDsFfc4Fpm?si=47b03d865274476a"}]
    
}

def adquirir_conhecimento(genero: str, energia: str, eh_curta: bool, musicas: list[Recomendacao]) -> bool:
    caracteristicas_musicas = (genero, energia, eh_curta)

    if caracteristicas_musicas in KNOWLEDGE_BASE:
        KNOWLEDGE_BASE[caracteristicas_musicas].extend(musicas)
    else:
        KNOWLEDGE_BASE[caracteristicas_musicas] = musicas

    print(f"Nova regra: {caracteristicas_musicas}: {musicas}")
    
