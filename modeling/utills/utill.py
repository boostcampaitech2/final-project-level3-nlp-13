import json
from typing import *


def read_config(json_file_dir: str) -> Dict:
    """
    arguments
        - json_file_dir: config 파일의 위치

    return
        - Dict

    summary
        - json 파일을 읽어서 dict로 반환

    """
    with open(json_file_dir) as f:
        config = json.load(f)

    return config
