import re

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
    if label == 1 or label == 2:
        return True
    return False

def is_positive(label:int, confidence:float):
    if label == 1 and confidence >= 0.85:
        return True
    return False
