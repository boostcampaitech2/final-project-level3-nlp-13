import pandas as pd

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
    confidence: int = Field(default=int)
    time: Optional[datetime] = Field(default_factory=datetime.now)
    label_beep: Optional[int] = None # 0: Common, 1: hate
    label_senti: Optional[int] = None # 0: Common, 1: Neg, 2: Pos
    confidence_beep: Optional[float] = None
    confidence_senti: Optional[float] = None
    is_question: Optional[str] = None


hate_speech = ['시발', '개새끼']
pos_list = ['좋아요']

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
    if '?' in comments.text:
        res['is_question'] = 1
        return JSONResponse(res)

    if 'ㅅㅂ' in comments.text:
        res['label_beep'] = 1
    else:
        res['label_beep'] = 0

    if '좋아' in comments.text:
        res['label_senti'] = 2
    elif '싫어요' in comments.text:
        res['label_senti'] = 1
    else:
        res['label_senti'] = 0

    res['confidence_beep'] = 0.76
    res['confidence_senti'] = 0.87
    res['is_question'] = 0

    return JSONResponse(res)

@router.post("/loadSampleLog")
def loadSampleLog():
    res = dict()    
    df = pd.read_csv('files/sample_log.csv')

    res['comments'] = df.to_dict('records')

    return JSONResponse(res)


