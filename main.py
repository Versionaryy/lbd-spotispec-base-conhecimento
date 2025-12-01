'''
Interface com o usuário + integração com Spotify
'''

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.models import Regra
from src.knowledge_base import adquirir_conhecimento
from fastapi.responses import JSONResponse
import logging



app = FastAPI(title="Lambda de aquisição de conhecimento para sistema especialista")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Rota recebida pelo FastAPI: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:5173",
#     "https://det60lfqy4fiv.cloudfront.net",
#     "https://d1x3sdynnsov76.cloudfront.net"
# ]
# app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["POST", "OPTIONS"], allow_headers=["*"])
@app.post("/prod/aquisicao-conhecimento") # o prod é uma gabiarra, perdão professor 🙏
def obter_recomendacao(regra: Regra):
    try:
        if not regra.musicas or len(regra.musicas) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"mensagem": "Nenhuma música fornecida na requisição"})

        musica = regra.musicas[0]
        sucesso, mensagem = adquirir_conhecimento(regra.genero, regra.energia, regra.eh_curta, musica)
        if sucesso:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": mensagem})
        else:
            content = mensagem if isinstance(mensagem, dict) else {"mensagem": mensagem}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"mensagem": str(e)})


handler = Mangum(app)