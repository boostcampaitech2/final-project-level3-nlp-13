from typing import Dict

from app.routers import chat, sample
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(chat.router)
app.include_router(sample.router)

templates = Jinja2Templates(directory="templates/")
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


@app.get("/")
def home():
    return {"hello": "world"}
