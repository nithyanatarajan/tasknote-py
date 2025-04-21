from fastapi import FastAPI

from .api.router import router

app = FastAPI()

app.include_router(router, prefix='/api')


@app.get('/')
async def root():
    return {'message': 'Welcome to the Notes API'}


@app.get('/health')
async def health():
    return {'status': 'OK'}
