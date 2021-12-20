from typing import *
import nltk
from nltk.tokenize import word_tokenize

from tqdm import tqdm
from logger.mylogger import set_logger
import emoji
from soynlp.normalizer import repeat_normalize
import re


def del_stopword(
        texts:str,
        )->str:
    '''
        arguments
            - texts: text들
        
        return type
            - str

        summary
            - text들을 받아 불용어 token을 제거한 text를 반환
    '''
    loger = set_logger()
    loger.info("Delete stop words")
    nltk.download('punkt')
    preprcessed_text = []
    stop_words = []
    with open('data/stop_words.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line: break
            stop_words.append(line)
    f.close()

    for text in tqdm(texts):
        word_tokens = word_tokenize(text)
        result = []
        for w in word_tokens:
            if w not in stop_words:
                result.append(w)
        preprcessed_text.append(' '.join(result))
    
    loger.info("Complete delete stop words!!")

    return preprcessed_text

def cleaning(texts):
    emojis = ''.join(emoji.UNICODE_EMOJI.keys())
    pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣{emojis}]+')
    url_pattern = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    
    loger = set_logger()
    loger.info("Cleaning sentence")

    preprcessed_text = []
    for text in tqdm(texts):
        text = pattern.sub(' ', str(text))
        text = url_pattern.sub('', text)
        text = text.strip()
        text = repeat_normalize(text, num_repeats=2)

        preprcessed_text.append(text)
    
    loger.info("Complete cleaning words!!")

    return preprcessed_text
