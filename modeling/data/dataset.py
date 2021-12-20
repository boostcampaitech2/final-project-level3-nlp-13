from typing import *
from torch.utils.data import Dataset
import torch
from transformers import AutoTokenizer
import pandas as pd
import os

from data.preprocessing import del_stopword, cleaning

class DatasetForHateSpeech(Dataset):
    def __init__(
        self, 
        type : str,
        tokenizer : AutoTokenizer,
        path : str,
        config : Dict,
        version : str = "v1",
    )->None:
        """
            Arguments:
                - type : 데이터 종류 , keywords=(train, valid, test) 
                - tokenizer : 토크나이저 종류
                - path: 데이터 경로
                - config: 각종 설정을 저장한 dict
                - version : 데이터 셋 버전
    
            Summary:
                Tokenizing 된 Hate Speech 데이터 셋 객체
        """
        self.path = os.path.join(path, f"{type}", f"data_{version}.tsv")
        self.data = pd.read_csv(self.path, sep="\t", encoding='utf-8')

        if 'stopwords' in config['data']['preprocessing']:
            self.data['comments'] = del_stopword(self.data['comments'].tolist())
        if 'cleaning' in config['data']['preprocessing']:
            self.data['comments'] = cleaning(self.data['comments'].tolist())

        self.tokenized_data = tokenizer(
            self.data['comments'].tolist(),#Sentence
            return_tensors="pt",
            return_token_type_ids=False,
            padding=True,
            truncation=True,
            max_length=50,
            add_special_tokens=True,
        )
        self.labels = self.data['label'].tolist()

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.tokenized_data.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.data)

class CurriculumDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer= tokenizer
        self.tokenized_text = tokenizer(
            self.data['comments'].tolist(),
            max_length = 50,
            padding=True,
            truncation=True,
            return_tensors='pt',
            return_token_type_ids=False
        )
    def __getitem__(self, idx):
        return {
            "input_ids" : self.tokenized_text['input_ids'][idx],
            "attention_mask" : self.tokenized_text['attention_mask'][idx]
        }, torch.tensor(self.data['label'].tolist()[idx])

    def __len__(self):
        return len(self.data)