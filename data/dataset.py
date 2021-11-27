from torch.utils.data import Dataset
from transformers import AutoTokenizer
import pandas as pd
import os

DATA_PATH = "../dataset/"

class DatasetForHateSpeech(Dataset):
    def __init__(
        self, 
        type : str,
        tokenizer : AutoTokenizer,
        version : str = "v1",
    )->None:
        """
            Arguments:
                - type : 데이터 종류 , keywords=(Train, Validation, Test) 
                - tokenizer : 토크나이저 종류
                - version : 데이터 셋 버전
    
            Summary:
                Tokenizing 된 Hate Speech 데이터 셋 객체
        """
        self.path = os.path.join(DATA_PATH,f"{type}",f"data_{version}.tsv")
        self.data = pd.read_csv(self.path, encoding='utf-8')

        self.tokenized_data = tokenizer(
            self.data['comments'].tolist(),
        )
        
        self.labels = self.data['label'].tolist()

    def __getitem__(self, idx):
        return self.tokenized_data[idx], self.labels[idx]

    def __len__(self):
        return len(self.data)

