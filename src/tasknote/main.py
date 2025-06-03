from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import router

app = FastAPI()

app.include_router(router, prefix='/tasknote')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
