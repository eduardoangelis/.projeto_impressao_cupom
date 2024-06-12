import uvicorn
import logging
import json
import base64
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from escpos.printer import Network
from fastapi import Request
from fastapi.logger import logger as fastapi_logger

# Configurar o logger
logging.basicConfig(level=logging.DEBUG)
gunicorn_logger = logging.getLogger('gunicorn.error')
fastapi_logger.handlers = gunicorn_logger.handlers



PRINTER_IP = "192.168.7.243"
PRINTER_PORT = 9100

class Item(BaseModel):
    parametro: str


# Função para decodificar um valor base64 tratando o erro de padding
def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data)


app = FastAPI(title="Endpoints Impressao")

# Configurando o middleware CORS (Cross-Origin Resource Sharing) para uma aplicação FastAPI
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                      # define quais origens estão autorizadas a fazer solicitações para este aplicativo
    allow_credentials=True,                     # define se o aplicativo aceita solicitações com credenciais
    allow_methods=["*"],                        # define quais métodos HTTP são permitidos para solicitações de origem cruzada
    allow_headers=["*"],                        # define quais cabeçalhos de solicitação de origem cruzada são permitidos
)


@app.post("/teste")
async def read_root(request: Request):
    data = {
  "parametro": "G2EBGyEATkZDLWUKGyEBG2EAR0NNIENPTUVSQ0lPIERFIExVQlJJRklDQU5URVMgTFREQQpDTlBKOjMzLjA5MC43MjEvMDAwMS05OSBJLkUuOjI4MjU2NTEwOApSVUEgQ09ST05FTCBQT05DSUFOTyBERSBNQVRUT1MgUEVSRUlSQSwgNDU1CkpBUkRJTSBDT0xJQlJJIC0gRE9VUkFET1MgLSBNUwpDRVA6IDc5ODM5LTA2MCAtIEZPTkU6ICg2NykgMzQyMC0xNDAwCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tChthAURPQ1VNRU5UTyBBVVhJTElBUgpEQSBOT1RBIEZJU0NBTCBERSBDT05TVU1JRE9SIEVMRVRST05JQ0EKG2EALS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KTkZDLWUgRW1pdGlkYSBlbSBBbWJpZW50ZSBkZSBUZXN0ZXMKU0VNIFZBTE9SIEZJU0NBTApORkMtZSBuYW8gcGVybWl0ZSBhcHJvdmVpdGFtZW50byBkZSBjcmVkaXRvIGRlIElDTVMKTnVtZXJvOjMwOSBTZXJpZTogMDA4IEVtaXNzYW86IDMxLzA1LzIwMjQgMTE6MDY6MjIKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KQ29uc3VsdGUgcGVsYSBDaGF2ZSBkZSBBY2Vzc28gZW0gCiAgICAgICAgICAgICBodHRwOi8vd3d3LmRmZS5tcy5nb3YuYnIvbmZjZSAgICAgICAgICAgICAgCkNIQVZFIERFIEFDRVNTTwogNTAyNCAwNTMzIDA5MDcgMjEwMCAwMTk5IDY1MDAgODAwMCAwMDAzIDA5MTEgMDAwMCAzMDk5IApDb25zdWx0YSB2aWEgbGVpdG9yIFFSIENvZGUKG2EBHWtRAwYIAf8AaHR0cDovL3d3dy5kZmUubXMuZ292LmJyL25mY2UvcXJjb2RlP3A9NTAyNDA1MzMwOTA3MjEwMDAxOTk2NTAwODAwMDAwMDMwOTExMDAwMDMwOTl8MnwyfDF8ODA2NzI3NkFGMjM1MjAwQjBDODdBMDczOUVBMTgzMTA1NDVDMjlBQiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgChthAFFVQU5USURBREUgVE9UQUwgREUgSVRFTlMgOiAxClZBTE9SIFRPVEFMIFIkIDMyLDQ3CkZPUk1BIERFIFBBR0FNRU5UTyBWQUxPUiBQQUdPCkNhcnRhbyBkZSBDcmVkaXRvICAgICAgIDMyLDQ3CkluZm9ybWFjYW8gZG9zIFRyaWJ1dG9zIEluY2lkZW50ZXMKKExlaSBGZXJkZXJhbCAxMi43NDEvMjAxMikgMCwwMCAwLDAwCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCkl0LiBDT0RJR08gICAgREVTQ1JJQ0FPIFFVQU5ULiBVTi4gVkwuVU5JVC4gICAgIFZMLlRPVEFMCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCjAwMSAwNDgwOCBOT1RBIEZJU0NBTCBFTUlUSURBIEVNIEFNQklFTlRFIERFIEhPTU9MT0cKICAgICAgICAgICAgICAgICAgICAgICAgMSwwMDAwIFVOIHggMzIsNDcwMCAgICAgICAgMzIsNDcKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KVkFMT1IgUFJPRFVUT1MvU0VSVklDT1MgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKVkFMT1IgVE9UQUwgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKUHJvdC4gQXV0b3JpemFjYW86IDE1MDI0MDAwMDA2MDA5NCAtIDMxLzA1LzIwMjQgMTE6MDY6MjcKUEFHQU1FTlRPUyA6CkNhcnRhbyBkZSBDcmVkaXRvICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKTUFTVEVSQ0FSRCAgICAgICAgICAgICAgICAgICAgICAgICAgICAwMS40MjUuNzg3LzAwMDEtMDQKCgo="
}
    print(data)
    data = await request.json()
    
    return {"message": "ok"}

@app.post("/")
async def imprimir(item: str = Body(...)):
    try:
        # Converter a string JSON em um objeto Python
        data = json.loads(item)

        #print(data['parametro'])
        fastapi_logger.debug('Iniciando a impressão...')
        p = Network(PRINTER_IP, PRINTER_PORT)
        p.set(align='center', width=2, height=2)


        
        fastapi_logger.debug('Decodificando o valor base64...')
        # Decodificar o valor base64
        decoded_parametro = decode_base64(data['parametro']).decode('ISO-8859-1')
        logging.debug(f'Valor decodificado: {decoded_parametro}')


        # Imprimir o valor decodificado
        fastapi_logger.debug('Imprimindo o valor decodificado...')
        print(decoded_parametro)
        p.text(decoded_parametro)
        p.cut()

        # Fechar a conexão com a impressora
        p.close()

        fastapi_logger.debug('Impressão concluída.')
        return {"message": "Impressão concluída"}

    except Exception as e:
        fastapi_logger.error(f'Erro durante a impressão: {str(e)}')
        return {"error": str(e)}






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008, log_level="info")