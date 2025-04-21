from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Welcome to the Notes API'}


@app.get('/health')
async def health():
    return {'status': 'OK'}
