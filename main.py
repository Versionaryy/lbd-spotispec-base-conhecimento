'''
Interface com o usuário + integração com Spotify
'''

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.models import Regra
from src.knowledge_base import adquirir_conhecimento

app = FastAPI(title="Lambda de aquisição de conhecimento para sistema especialista")

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:5173",
#     "https://det60lfqy4fiv.cloudfront.net"
# ]
# app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["POST", "OPTIONS"], allow_headers=["*"])
@app.post("/aquisicao-conhehcimento") # o prod é uma gabiarra, perdão professor 🙏
def obter_recomendacao(regra: Regra):
    # try:
        adquirir_conhecimento(**regra.dict())
        return {"codigo": status.HTTP_200_OK, "mensagem": "musica adicionada"}
    # except Exception as e:
    #     return e


handler = Mangum(app)