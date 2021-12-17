from typing import *

import torch
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
from transformers import PreTrainedTokenizerFast

def get_model(
        model_name: str,
        model_type: str = 'huggingface',
        num_classes: int = 2,
    ):
    '''
        arguments
            - model_name : str
                모델의 이름을 반환 허깅페이스의 경우 pretrained 모델의 이름
                커스텀 모델의 경우 클래스 이름
            - model_type : str
                huggingface or custom

        return
            - torch.nn.module

        summary
            - 모델의 이름과 타입에 따라 학습 및 추론에 사용할 모델 반환
    '''

    if model_type == 'huggingface':
        model_config = AutoConfig.from_pretrained(model_name)
        model_config.num_labels = num_classes    
        model = AutoModelForSequenceClassification.from_pretrained(model_name, config=model_config)    
    elif model_type == 'pretrained':
         model_config = AutoConfig.from_pretrained(model_name + '/config.json')
         model_config.num_labels = num_classes    
         model = AutoModelForSequenceClassification.from_pretrained(model_name, config=model_config)
         #state_dicts = torch.load(model_name + '/pytorch_model.bin')
         #model.load_state_dict(state_dicts)
    elif model_type == 'custom':
        print(num_classes, model_name)
    

    return model

def get_tokenizer(
        tokenizer_name: str,
        tokenizer_type: str = 'huggingface',
    ):
    '''
        arguments
            tokenizer_name : str
                토크나이저의 이름을 반환 허깅페이스의 경우 pretrained 모델의 이름
                커스텀 토크나이저의 경우 클래스 이름
            tokenizer_type : str
                huggingface or custom

        return
            AutoTokenizer

        summary
            토크나이저의 이름과 타입에 따라 학습 및 추론에 사용할 모델 반환
    '''

    if tokenizer_type == 'huggingface':
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    elif tokenizer_type == 'char_level':
        tokenizer = PreTrainedTokenizerFast(tokenizer_file="/opt/ml/trained_tok/vocab.json")
        tokenizer.bos_token="[SOS]"
        tokenizer.eos_token="[EOS]"
        tokenizer.sep_token="[SEP]"
        tokenizer.cls_token="[SOS]"
        tokenizer.unk_token="[UNK]"
        tokenizer.pad_token="[PAD]"
        tokenizer.mask_token="[MASK]"
    elif tokenizer_type == 'custom':
        print(tokenizer_name)

    return tokenizer

def get_optimizer(
        optimizer_name:str
    ):
    '''
        arguments
            optimizer_name : str
                학습에 사용할 옵티마이저 이름

        return
            Optimizer

        summary
            옵티마이저 반환
    '''
    print('아직 미사용')