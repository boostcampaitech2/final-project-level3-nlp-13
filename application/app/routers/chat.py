from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from typing import Optional

from datetime import date, datetime

class Comments(BaseModel):

    user_id: str = Field(default=str)
    text: str = Field(default=str)
    time: Optional[datetime] = Field(default_factory=datetime.now)
    label_beep: Optional[int] = None
    label_senti: Optional[int] = None
    confidence_beep: Optional[float] = None
    confidence_senti: Optional[float] = None
    is_question: Optional[str] = None


hate_speech = ['시발', '개새끼']

router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="templates/")
router.mount("/statics", StaticFiles(directory="statics"), name="statics")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@router.post("/sendMessage", response_model=Comments)
def sendMessage(comments: Comments):

    print('================= sendMessage ==================')
    print(comments)
    res = dict(comments)

    res['time'] = res['time'].strftime('%Y-%m-%d %H:%M:%S')
    res['label_beep'] = 0
    res['label_senti'] = 1
    res['confidence_beep'] = 0.76
    res['confidence_senti'] = 0.87
    res['is_question'] = 0

    return JSONResponse(res)