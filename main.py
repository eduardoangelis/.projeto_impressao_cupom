from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
import base64
import uvicorn
from escpos.printer import Network
from fastapi import Request
import logging

logging.basicConfig(level=logging.DEBUG)

PRINTER_IP = "192.168.7.243"
PRINTER_PORT = 9100

class Item(BaseModel):
    parametro: str


def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data)


app = FastAPI(title="Endpoints Impressao")


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/teste")
async def read_root(request: Request):
    data = {
  "parametro": "G2EBGyEATkZDLWUKGyEBG2EAR0NNIENPTUVSQ0lPIERFIExVQlJJRklDQU5URVMgTFREQQpDTlBKOjMzLjA5MC43MjEvMDAwMS05OSBJLkUuOjI4MjU2NTEwOApSVUEgQ09ST05FTCBQT05DSUFOTyBERSBNQVRUT1MgUEVSRUlSQSwgNDU1CkpBUkRJTSBDT0xJQlJJIC0gRE9VUkFET1MgLSBNUwpDRVA6IDc5ODM5LTA2MCAtIEZPTkU6ICg2NykgMzQyMC0xNDAwCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tChthAURPQ1VNRU5UTyBBVVhJTElBUgpEQSBOT1RBIEZJU0NBTCBERSBDT05TVU1JRE9SIEVMRVRST05JQ0EKG2EALS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KTkZDLWUgRW1pdGlkYSBlbSBBbWJpZW50ZSBkZSBUZXN0ZXMKU0VNIFZBTE9SIEZJU0NBTApORkMtZSBuYW8gcGVybWl0ZSBhcHJvdmVpdGFtZW50byBkZSBjcmVkaXRvIGRlIElDTVMKTnVtZXJvOjMwOSBTZXJpZTogMDA4IEVtaXNzYW86IDMxLzA1LzIwMjQgMTE6MDY6MjIKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KQ29uc3VsdGUgcGVsYSBDaGF2ZSBkZSBBY2Vzc28gZW0gCiAgICAgICAgICAgICBodHRwOi8vd3d3LmRmZS5tcy5nb3YuYnIvbmZjZSAgICAgICAgICAgICAgCkNIQVZFIERFIEFDRVNTTwogNTAyNCAwNTMzIDA5MDcgMjEwMCAwMTk5IDY1MDAgODAwMCAwMDAzIDA5MTEgMDAwMCAzMDk5IApDb25zdWx0YSB2aWEgbGVpdG9yIFFSIENvZGUKG2EBHWtRAwYIAf8AaHR0cDovL3d3dy5kZmUubXMuZ292LmJyL25mY2UvcXJjb2RlP3A9NTAyNDA1MzMwOTA3MjEwMDAxOTk2NTAwODAwMDAwMDMwOTExMDAwMDMwOTl8MnwyfDF8ODA2NzI3NkFGMjM1MjAwQjBDODdBMDczOUVBMTgzMTA1NDVDMjlBQiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgChthAFFVQU5USURBREUgVE9UQUwgREUgSVRFTlMgOiAxClZBTE9SIFRPVEFMIFIkIDMyLDQ3CkZPUk1BIERFIFBBR0FNRU5UTyBWQUxPUiBQQUdPCkNhcnRhbyBkZSBDcmVkaXRvICAgICAgIDMyLDQ3CkluZm9ybWFjYW8gZG9zIFRyaWJ1dG9zIEluY2lkZW50ZXMKKExlaSBGZXJkZXJhbCAxMi43NDEvMjAxMikgMCwwMCAwLDAwCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCkl0LiBDT0RJR08gICAgREVTQ1JJQ0FPIFFVQU5ULiBVTi4gVkwuVU5JVC4gICAgIFZMLlRPVEFMCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCjAwMSAwNDgwOCBOT1RBIEZJU0NBTCBFTUlUSURBIEVNIEFNQklFTlRFIERFIEhPTU9MT0cKICAgICAgICAgICAgICAgICAgICAgICAgMSwwMDAwIFVOIHggMzIsNDcwMCAgICAgICAgMzIsNDcKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KVkFMT1IgUFJPRFVUT1MvU0VSVklDT1MgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKVkFMT1IgVE9UQUwgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKUHJvdC4gQXV0b3JpemFjYW86IDE1MDI0MDAwMDA2MDA5NCAtIDMxLzA1LzIwMjQgMTE6MDY6MjcKUEFHQU1FTlRPUyA6CkNhcnRhbyBkZSBDcmVkaXRvICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMzIsNDcKTUFTVEVSQ0FSRCAgICAgICAgICAgICAgICAgICAgICAgICAgICAwMS40MjUuNzg3LzAwMDEtMDQKCgo="
}
    #data = await request.json()
    print(data)
    return {"message": data}

@app.post("/")
async def imprimir(item: Item):
    try:
        print(item.parametro)
        logging.debug('Iniciando a impressão...')
        p = Network(PRINTER_IP, PRINTER_PORT)
        p.set(align='center', width=2, height=2)


        
        logging.debug('Decodificando o valor base64...')
        # Decodificar o valor base64
        #decoded_parametro = base64.b64decode(item.parametro).decode('utf-8')
        decoded_parametro = decode_base64(item.parametro).decode('ISO-8859-1')
        logging.debug(f'Valor decodificado: {decoded_parametro}')


        # Imprimir o valor decodificado
        logging.debug('Imprimindo o valor decodificado...')
        p.text(decoded_parametro)
        p.cut()

        # Fechar a conexão com a impressora
        p.close()

        logging.debug('Impressão concluída.')
        return {"message": "Impressão concluída"}

    except Exception as e:
        logging.error(f'Erro durante a impressão: {str(e)}')
        return {"error": str(e)}






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008, log_level="debug")