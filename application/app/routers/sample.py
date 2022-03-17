from fastapi import FastAPI, Request, Form, APIRouter, requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter(prefix="/sample")
templates = Jinja2Templates(directory="templates/")


class User(BaseModel):
    name: str
    comment: str


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("sample.html", {"request": request})


@router.post("/form_post", response_class=User)
def form_post(user: User):
    print("form_post called...")
    print(user)
    res = dict(user)
    res["message"] = "hello! " + user.name
    return JSONResponse(res)
