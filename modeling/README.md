# 데이터셋
## 악성 채팅 분류
- [욕설 감지 데이터 셋](https://github.com/2runo/Curse-detection-data)

- [Korean Hate Speech Dataset](https://www.kaggle.com/captainnemo9292/korean-hate-speech-dataset/metadata)

- [Korean Hate Speech Detection](https://github.com/kocohub/korean-hate-speech)

## 감성 분류 모델
- [nsmc](https://github.com/e9t/nsmc)

- [감성 분석용 말뭉치(네이버 쇼핑 리뷰, 스팀 리뷰)](https://github.com/bab2min/corpus/tree/master/sentiment)

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

## Paper

- [ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555)

- [Don't Stop Pretraining: Adapt Language Models to Domains and Tasks](https://arxiv.org/abs/2004.10964)

- [Curriculum Learning for Natural Language Understanding](https://aclanthology.org/2020.acl-main.542.pdf)

- [BEEP! Korean Corpus of Online News Comments for Toxic Speech Detection](https://arxiv.org/abs/2005.12503)


- [Learning Loss for Active Learning
](https://arxiv.org/abs/1905.03677)
