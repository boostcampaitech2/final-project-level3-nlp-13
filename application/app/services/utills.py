from typing import Dict, List

import re
from konlpy.tag import Mecab

class ClassType:
    HATE = 1
    OFFENSIVE = 0
    POSITIVE = 1
    NEGATIVE = 0
    NORMAL = 2

def is_FAQ(text: str):
    '''주어진 문장이 질문의 형태인지 아닌지 판단하여 반환'''

    if '궁금' in text:
        return True
    comp = re.compile(r'[가-힣a-zA-Zㄱ-ㅎㅏ-ㅣ]{2,}[?]$')
    sub_text = a = comp.findall(text)
    if sub_text:
        return True
    return False

def is_greeting(text: str):
    '''주어진 문장이 인사의 형태인지 아닌지 판단하여 반환'''

    if '안녕' in text or 'ㅎㅇ' in text:
        return True
    return False

def is_beep(label: int, confidence: float, base: float):
    '''주어진 문장이 악성인지 아닌지 class와 confidence 값을 활용해 최종 class 결정'''

    if (label == ClassType.HATE or label == ClassType.OFFENSIVE) and confidence >= base:
        return True
    return False

def is_positive(label: int, confidence: float, base: float):
    '''주어진 문장이 긍정인지 부정인지 class와 confidence 값을 활용해 최종 class 결정'''

    if label == ClassType.POSITIVE and confidence >= base:
        return True
    if label == ClassType.NEGATIVE and confidence >= base:
        return True
    return False

def check_beep_dictionary(text: str, beep_dic: List):
    '''주어진 문장에 욕설 사전에 포함된 문장이 있는지 없는지 판단'''
    for beep_word in beep_dic:
        if beep_word in text:
            return True
    return False

def update_wc(input_text: str, word_cloud_dict: Dict):
    '''word cloud를 나타내기 위한 word dict 업데이트'''

    mecab = Mecab()
    for n in mecab.nouns(input_text):
        word_cloud_dict[n] += 1

    
