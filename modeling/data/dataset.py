from typing import *
from torch.utils.data import Dataset
from transformers import AutoTokenizer
import pandas as pd
import os

from data.preprocessing import del_stopword

#DATA_PATH = "../dataset/"

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

        self.tokenized_data = tokenizer(
            self.data['comments'].tolist(),#Sentence
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
            add_special_tokens=True,
        )
        self.labels = self.data['label'].tolist()

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.tokenized_data.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.data)

class DatasetForSentimentSpeech(Dataset):
    def __init__(
        self, 
        tokenizer : AutoTokenizer,
        path : str,
    ) -> None:
        """
            Arguments:
                - tokenizer : 토크나이저 종류
                - path : 데이터 저장된 경로
            Summary:
                Tokenizing 된 감성 분류 데이터 셋 객체
        """
        self.data = pd.read_csv(path)
        self.data = self.data.dropna(axis=0) 

        self.tokenized_data = tokenizer(
            self.data['document'].tolist(),#Sentence
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
            add_special_tokens=True,
        )

        self.labels = self.data['label'].tolist()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.tokenized_data.items()}
        item['labels'] = self.labels[idx]
        return item