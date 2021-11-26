from typing import *
from transformers import 

def get_model(
        model_name: str,
        model_type: str = 'huggingface',
    ):

    if model_type == 'huggingface':

