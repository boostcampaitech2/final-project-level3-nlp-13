from typing import *

import torch

from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer

'''
class_dict = {
    0: 'None',
    1: 'Hate',
    2: 'Hate',
}
'''

def get_model(model_kind:str, model_name:str='beomi/KcELECTRA-base')->AutoModelForSequenceClassification:
    '''모델 가져오기'''

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    '''
    confing = AutoConfig.from_pretrained(model_name)
    model = AutoModelForSequenceClassification(config=config)
    state_dicts = torch.load('./models/weights/' + 'beep_best.bin')
    model.load_state_dict(state_dicts)
    '''
    return model

def get_tokenizer(model_name:str='beomi/KcELECTRA-base')->AutoTokenizer:
    '''토크나이져 가져오기'''

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer

def predict_from_text(
    model: AutoModelForSequenceClassification,
    tokenizer: AutoTokenizer,
    text: str) -> Union[int, float]:
    '''text를 받아 악성 댓글 여부를 판단하여 반환'''
    
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=50,
        add_special_tokens=True,
    )
    pred = model(input_ids = inputs['input_ids'].to(device))
    classes = torch.argmax(pred['logits'].detach()).detach().item()
    confidence = torch.max(pred['logits'].detach()).detach().item()
    return classes, confidence