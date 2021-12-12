from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse

class Chat(BaseModel):
    """[summary]
        {
            "user_info" : {"id" : 'rkdqus2006'},
            "message" : {"text" : '반갑습니다 행님들'},
            "model_result" : {"sentiment":0, "is_hate":0} ()
        }
    Args:
        BaseModel ([type]): [description]
    """
    user_info: dict
    message: dict
    model_result : dict

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
    print(chat)


    return JSONResponse(res)