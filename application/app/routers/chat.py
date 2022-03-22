import json
import time
from collections import defaultdict
from datetime import date, datetime
from typing import *
from typing import Optional

import pandas as pd
from app.models.model import get_model, get_tokenizer, make_inference
from app.services.utills import (ClassType, check_beep_dictionary, is_FAQ,
                                 is_greeting, is_positive, update_wc)
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from pytz import timezone
from starlette.responses import JSONResponse


class Comments(BaseModel):
    user_id: str = Field(default=str)
    text: str = Field(default=str)
    confidence: int = Field(default=int)
    time: Optional[datetime] = Field(
        default_factory=datetime.now(timezone("Asia/Seoul")).now
    )
    label_beep: Optional[str] = None  # 0: Offensive, 1: hate, 2: Common
    label_senti: Optional[int] = None  # 0: Pos 1: Neg, 2: Common
    confidence_beep: Optional[float] = None
    confidence_senti: Optional[float] = None
    is_question: Optional[bool] = None


router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="templates/")
router.mount("/statics", StaticFiles(directory="statics"), name="statics")

hate_or_none_model = None
offensive_or_none_model = None
beep_tokenizer = None
senti_model = None
senti_tokenizer = None

beep_dic = defaultdict(str)
pos_word_cloud_dict = defaultdict(int)
neg_word_cloud_dict = defaultdict(int)


@router.on_event("startup")
def init():
    """
    Summary:
        초기 실행시, 필요한 모델과 토크나이저 및 dictionary들 로딩
    """
    # 1. 악성 모델 로딩
    global hate_or_none_model, offensive_or_none_model, beep_tokenizer, senti_model, senti_tokenizer, beep_dic
    if hate_or_none_model is None:
        hate_or_none_model = get_model(
            model_kind="hate.bin", numlabels=2, type="bin", model_name="custom"
        )
    if offensive_or_none_model is None:
        offensive_or_none_model = get_model(
            model_kind="offensive.bin", numlabels=2, type="bin", model_name="custom"
        )

    if beep_tokenizer is None:
        beep_tokenizer = get_tokenizer()

    # 2. 감성 모델 로딩
    if senti_model is None:  #'monologg/koelectra-base-finetuned-nsmc'
        senti_model = get_model(
            model_kind="roti_final.pt",
            numlabels=2,
            model_name="monologg/koelectra-base-finetuned-nsmc",
            type="pt",
        )
    if senti_tokenizer is None:
        senti_tokenizer = get_tokenizer(
            model_name="monologg/koelectra-base-finetuned-nsmc"
        )

    # 3. 각종 사전 로딩
    with open("files/abuse_voca.json") as f:
        data = json.load(f)
    beep_dic = pd.DataFrame(data)["badwords"].tolist()


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
    """
    Arguments:
        - chat: 유저의 채팅에 대한 메타정보 딕셔너리

    Returns:
        int, float

    Summary:
        유저의 채팅 내용, 모델, 토크나이저를 입력받아 모델에 따른 분석결과를 활용해 post processing을 적용
        최종 결과를 반환
    """
    start = time.time()  # 시작 시간 저장
    res = dict(comments)
    res["time"] = res["time"].strftime("%Y-%m-%d %H:%M:%S")
    preprocessed_text = res["text"]

    # 1. 인사인가?
    if is_greeting(preprocessed_text):
        return JSONResponse(res)

    # 2. 감성 분석
    senti_inference_result, senti_confidence = make_inference(
        preprocessed_text, senti_model, senti_tokenizer
    )

    # 결과 class 및 confidence에 따른 class 변경
    if not is_positive(
        senti_inference_result, senti_confidence, float(res["confidence"]) / 100
    ):
        senti_inference_result = ClassType.NORMAL

        # 결과 저장
    res["label_senti"] = senti_inference_result
    res["confidence_senti"] = senti_confidence
    # Word cloud 업데이트
    if senti_inference_result == ClassType.NEGATIVE:
        update_wc(res["text"], neg_word_cloud_dict)
    elif senti_inference_result == ClassType.POSITIVE:
        update_wc(res["text"], pos_word_cloud_dict)

    # 3. 악성 분석
    # 3-1. 직접적 욕설 포함?
    if check_beep_dictionary(preprocessed_text, beep_dic):
        res["label_beep"] = ClassType.HATE
        res["confidence_beep"] = 1.0
        print("time :", time.time() - start)
        return JSONResponse(res)
    else:
        beep_inference_result, _ = make_inference(
            preprocessed_text, hate_or_none_model, beep_tokenizer
        )
        if beep_inference_result == ClassType.HATE:
            res["label_beep"] = "Hate"
        # None 으로 판단시 Offensive/None 분류
        if beep_inference_result != ClassType.HATE:
            beep_inference_result, _ = make_inference(
                preprocessed_text, offensive_or_none_model, beep_tokenizer
            )
            if beep_inference_result == ClassType.OFFENSIVE:
                res["label_beep"] = "Offensive"

    # 욕설이 아니면 질문으로 분류
    if res["label_beep"] not in [
        "Hate",
        "Offensive",
    ]:  # != ClassType.HATE and beep_inference_result != ClassType.OFFENSIVE:
        beep_inference_result = ClassType.NORMAL
        res["label_beep"] = "None"  # beep_inference_result
        res["confidence_beep"] = _  # 사용하지 않음
        if is_FAQ(preprocessed_text):
            # FAQ 따로 저장
            res["is_question"] = True
            print("time :", time.time() - start)
            return JSONResponse(res)

    # 부정이고 욕설이면 최종으로 욕설로 판단
    # if senti_inference_result == ClassType.NEGATIVE and (beep_inference_result == ClassType.HATE or beep_inference_result == ClassType.OFFENSIVE):
    #     beep_inference_result = ClassType.HATE
    # res['label_beep'] = beep_inference_result
    # res['confidence_beep'] = _

    print("time :", time.time() - start)
    return JSONResponse(res)


@router.post("/loadSampleLog")
def loadSampleLog():
    res = dict()
    df = pd.read_csv("files/sample_final.csv")

    res["comments"] = df.to_dict("records")

    return JSONResponse(res)


@router.post("/getWC")
def get_wc():
    res = dict()
    pos_json = [
        {"x": noun, "value": freq, "category": "pos"}
        for noun, freq in pos_word_cloud_dict.items()
    ]
    neg_json = [
        {"x": noun, "value": freq, "category": "neg"}
        for noun, freq in neg_word_cloud_dict.items()
    ]
    res["data"] = pos_json + neg_json

    return JSONResponse(res)
