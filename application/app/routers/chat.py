from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse

class Chat(BaseModel):
    user: str
    age: str
    message: str

hate_speech = ['시발', '개새끼']

router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="templates/")
router.mount("/statics", StaticFiles(directory="statics"), name="statics")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """[summary]
    open page
    Args:
        request (Request): HttpRequest
    Returns:
        HTMLResponse: html 형태로 리턴
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@router.post("/sendMessage", response_model=Chat)
def sendMessage(chat: Chat):
    res = dict(chat)

    if res['message'] in hate_speech:
        res['status'] = 'hate'
    else:
        res['status'] = 'normal'

    return JSONResponse(res)