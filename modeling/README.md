# 데이터셋

# trained model weights

# 프로젝트 구조
```
modeling/
│  example_config.json
│  train.py
│
├─data
│      abuse_words.txt
│      dataset.py
│      preprocessing.py
│      stop_words.txt
│      __init__.py
│
├─logger
│      mylogger.py
│
├─logs
├─models
│      custom.py
│      utill.py
│
├─train_utills
│      test.py
│      trainer_setting.py
│
└─utills
        utill.py
```
# Config

```json
{
    "data": {
        "train_data_path" : "../../hate_data/",
        "train_data_version" : "v2",
        "valid_data_path" : "../../hate_data/",
        "valid_data_version" : "v2",
        "test_data_path" : "../../hate_data/",
        "test_data_version" : "v2",
        "preprocessing" : ""
    },
    "model": {
        "model_name": "KoELECTRA",
        "model_type": "huggingface", #huggingface, pretrained, custom
        "num_classes": 3
    },
    "tokenizer": {
        "tokenizer_name": "KoELECTRA",
        "tokenizer_type": "huggingface" #huggingface, char_level, custom
    },
    "train":{
        "do_train": true,
        "epochs" : 30,
        "learning_rate": 5e-5,
        "save_total_limit": 2,
        "save_strategy": "steps",
        "evaluation_strategy": "steps",
        "train_batch_size": 32,
        "eval_batch_size" : 32,
        "warm_up_step" : 500,
        "weight_decay" : 0.01,
        "report": "wandb",
        "load_best_model_at_end": true
    },
    "test":{
        "do_test": true
    },
    "output": {
        "model_save_dir": "./results/KoELECTRA/",
        "result_save_path": "./outputs/"
    },
    "wandb": {
        "run_name": "KoELECTRA-"

    }
}
```

# Train

```
train.py -c <config dir>
```

# Inference
- config에서 do test ture로 설정 후 train.py 실행

        ```json
        "test":{
                "do_test": true
            },
        ```

# 모델 성능 및 학습 결과


# Reference
