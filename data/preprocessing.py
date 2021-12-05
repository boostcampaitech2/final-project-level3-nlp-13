from typing import *
import nltk
from nltk.tokenize import word_tokenize

from tqdm import tqdm
from logger.mylogger import set_logger

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