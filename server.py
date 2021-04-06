
from fastapi import FastAPI

from merval_socket import get_merval_data, start, stop

app = FastAPI()


@app.on_event('startup')
async def startup():
    print('starting up...')
    print('starting websocket...')
    start()


@app.on_event('shutdown')
async def shutdown():
    print('shutting down...')
    print('closing websocket...')
    stop()


@app.get('/asset/{ticker}')
async def price(ticker: str):
    return get_merval_data(ticker.upper())
