from typing import Dict

import re
from konlpy.tag import Mecab

HATE = 1
OFFENSIVE = 0
POSITIVE = 1
NEGATIVE = 0
NORMAL = 2

def is_FAQ(text:str):
    if '궁금' in text:
        return True
    comp = re.compile(r'[가-힣a-zA-Zㄱ-ㅎㅏ-ㅣ]{2,}[?]$')
    sub_text = a = comp.findall(text)
    if sub_text:
        return True
    return False

def is_greeting(text:str):
    if '안녕' in text or 'ㅎㅇ' in text:
        return True
    return False

def is_beep(label:int, confidence:float, base:float):
    if (label == HATE or label == OFFENSIVE) and confidence >= base:
        return True
    return False

def is_positive(label:int, confidence:float, base:float):
    if label == POSITIVE and confidence >= base:
        return True
    if label == NEGATIVE and confidence >= base:
        return True
    return False

def update_wc(input_text: str, word_cloud_dict:Dict):
    mecab = Mecab()
    for n in mecab.nouns(input_text):
        word_cloud_dict[n] += 1

    
