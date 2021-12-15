from typing import *
from fastapi import Request, Form, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from typing import Optional

from datetime import date, datetime
from models.model import get_model, get_tokenizer, predict_from_text
from services.utills import is_FAQ, is_greeting

from transformers import AutoModelForSequenceClassification, AutoTokenizer

class Comments(BaseModel):
    user_id: str = Field(default=str)
    text: str = Field(default=str)
    time: Optional[datetime] = Field(default_factory=datetime.now)
    label_beep: Optional[int] = None
    label_senti: Optional[int] = None
    confidence_beep: Optional[float] = None
    confidence_senti: Optional[float] = None
    is_question: Optional[bool] = None


router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="templates/")
router.mount("/statics", StaticFiles(directory="statics"), name="statics")

beep_model = None
beep_tokenizer = None
senti_model = None
senti_tokenizer = None

@router.on_event("startup")
def init():
    '''
        Summary:
            초기 실행시, 필요한 모델과 토크나이저 및 dictionary들 로딩
    '''
    # 1. 악성 모델 로딩
    global beep_model, beep_tokenizer, senti_model, senti_tokenizer
    if beep_model is None:
        beep_model = get_model(model_kind='beep_best.bin')
    if beep_tokenizer is None:
        beep_tokenizer = get_tokenizer()
    
    # 2. 감성 모델 로딩
    if senti_model is None:
        senti_model = get_model(model_kind='senti_best.pt', model_name='monologg/koelectra-small-v3-discriminator')
    if senti_tokenizer is None:
        senti_tokenizer = get_tokenizer(model_name='monologg/koelectra-small-v3-discriminator')

    # 3. 각종 사전 로딩
        # 욕설, 인사, 질문 등

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """[summary]
        open page
        Arguments:
            request (Request): HttpRequest

        Returns:
            HTMLResponse: html 형태로 리턴
    """
    return templates.TemplateResponse("chat.html", {"request": request})

@router.post("/sendMessage", response_model=Comments)
def sendMessage(comments: Comments):
    '''
        Arguments:
            - chat: 유저의 채팅에 대한 메타정보 딕셔너리

        Returns:
            int, float

        Summary:
            유저의 채팅 내용, 모델, 토크나이저를 입력받아 모델에 따른 분석결과를 활용해 post processing을 적용
            최종 결과를 반환
    '''
    res = dict(comments)
    preprocessed_text = res['text']

    # 1. 질문인가? 인사인가?
    if is_FAQ(preprocessed_text):
        # FAQ 따로 저장
        res['is_question'] = True
        return JSONResponse(res)

    if is_greeting(preprocessed_text):
        return JSONResponse(res)

    # 2. 감성 분석
    senti_inference_result, senti_confidence = make_inference(preprocessed_text, senti_model, senti_tokenizer)
        # To Do.
            # 결과 class 및 confidence에 따른 class 변경

    # 3. 악성 분석
        # 3-1. 직접적 욕설 포함?
    if False:
        # To Do.
            # preprocessed_text 알맞은 형태로 변경 
        print("직접적인 욕설이 있음")
    else:
        beep_inference_result, beep_confidence = make_inference(preprocessed_text, beep_model, beep_tokenizer)
        # To Do.
            # preprocessed_text 알맞은 형태로 변경 
            # 결과 class 및 confidence에 따른 class 변경
            # 악성 댓글이면 유저 카운트 증가

    # 4. 댓글 판단 결과 저장
    res['label_senti'] = senti_inference_result
    res['label_beep'] = beep_inference_result
    res['confidence_senti'] = senti_confidence
    res['confidence_beep'] = beep_confidence
 
    # 5. 판단 결과에 따라 post_processing
    res['message']['text'] = preprocessed_text # 부적절한 채팅입니다.

    return JSONResponse(res)

def make_inference(
        text: str,
        model: AutoModelForSequenceClassification,
        tokenizer: AutoTokenizer
                     )->Union[int, float]:
    '''
        Arguments:
            - text: 유저의 채팅 내용
            - model: 악성 또는 감성 분석 모델
            - tokenizer: 악성 또는 감성 분석 모델의 토크나이저

        Returns:
            int, float

        Summary:
            유저의 채팅 내용, 모델, 토크나이저를 입력받아 모델에 따른 분석결과를 반환
    '''
    try:
        inference_result, confidence = predict_from_text(model=model, tokenizer=tokenizer, text=text)
    except:
        raise HTTPException(status_code=404, detail=f"예측과정에서 오류가 발생했습니다. [text: {text}]")

    return inference_result, confidence