
from fastapi import FastAPI

from appSettings import AppSettings
from merval_data import MervalData
from merval_socket import MervalSocket

merval_data = MervalData()
appSettings = AppSettings()
merval_socket = MervalSocket(merval_data, appSettings.config)

app = FastAPI()


@app.on_event('startup')
async def startup():
    print('starting up RESTful server...')
    merval_socket.start()


@app.on_event('shutdown')
async def shutdown():
    print('shutting down RESTful server...')
    merval_socket.stop()


@app.get('/asset/{ticker}')
async def price(ticker: str):
    return merval_data.get_merval_data(ticker.upper())
