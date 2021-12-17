import re

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

def is_beep(label:int):
    if label == HATE or label == OFFENSIVE:
        return True
    return False

def is_positive(label:int, confidence:float):
    if label == POSITIVE and confidence >= 0.85:
        return True
    if label == NEGATIVE and confidence >= 0.85:
        return True
    return False
