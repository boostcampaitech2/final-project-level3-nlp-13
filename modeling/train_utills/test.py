import json
import os
from glob import glob
from typing import *

import torch
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


def load_best_model(model_dir: str, model):
    """
    Arguments
        - model_dir: 모델이 저장되어 있는 경로
        - model: weight를 불러올 모델

    Return
        - model

    Summary
        - 저장 경로를 탐색해 best 모델을 로딩하여 반환
    """
    weight_list = glob(model_dir + "*")
    weight_list = sorted(weight_list, key=lambda x: int(x.split("-")[-1]))

    model.load_state_dict(torch.load(weight_list[-1] + "/pytorch_model.bin"))
    print(f"load complete!! {weight_list[-1]}")
    return model


def do_test(config: Dict, model, test_dataset: Dataset):
    """
    Arguments
        - config: 학습 및 평가를 위한 여러가지 설정이 담겨있는 딕셔너리
        - model: 학습된 모델의 구조
        - test_dataset: test를 하기 위한 데이터 셋 (comments, labels)

    Return
        - Dict

    Summary
        - teset dataset을 이용해 metric 및 inference time test를 진행
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = load_best_model(config["output"]["model_save_dir"], model)
    model = model.to(device)

    dataloader = DataLoader(test_dataset, batch_size=1)

    result = {
        "inference": [],
        "real": [],
        "time": {
            "runtime": 0,
            "inference": [],
        },
        "accuracy": float("inf"),
        "f1-score": float("inf"),
    }

    time_measure_inference = 0
    for item in tqdm(dataloader):
        t_start = torch.cuda.Event(enable_timing=True)
        t_end = torch.cuda.Event(enable_timing=True)

        t_start.record()
        pred = model(
            input_ids=item["input_ids"].to(device),
            attention_mask=item["attention_mask"].to(device),
        )
        pred = torch.argmax(pred["logits"])

        t_end.record()
        torch.cuda.synchronize()
        t_inference = t_start.elapsed_time(t_end) / 1000
        time_measure_inference += t_inference

        result["inference"].append(int(pred.detach()))
        result["real"].append(int(item["labels"].detach().cpu()))
        result["time"]["inference"].append(t_inference)

    result["time"]["runtime"] = time_measure_inference

    result["f1-score"] = f1_score(result["real"], result["inference"], average="macro")
    result["accuracy"] = accuracy_score(result["real"], result["inference"])

    j = json.dumps(result, indent=4)
    save_path = os.path.join(
        config["output"]["result_save_path"], config["wandb"]["run_name"] + ".json"
    )
    with open(save_path, "w") as outfile:
        json.dump(result, outfile)

    return result
