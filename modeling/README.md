# 데이터셋
## 악성 채팅 분류
- [욕설 감지 데이터 셋](https://github.com/2runo/Curse-detection-data)

- [Korean Hate Speech Dataset](https://www.kaggle.com/captainnemo9292/korean-hate-speech-dataset/metadata)

- [Korean Hate Speech Detection](https://github.com/kocohub/korean-hate-speech)

## 감성 분류 모델
- [nsmc](https://github.com/e9t/nsmc)

- [감성 분석용 말뭉치(네이버 쇼핑 리뷰, 스팀 리뷰)](https://github.com/bab2min/corpus/tree/master/sentiment)

# trained model weights
```python
from transformers import ElectraModel
```
|Data Usage|num_labels|label's meaing
|:---|:---:|---|
|[BEEP only](https://drive.google.com/file/d/1DG3Ql7MXPFwRUiT7ajwur8jDTW46pkKY/view?usp=sharing)|3|0:none, 1:offensive, 2:hate
|[BEEP only, 2stage, hate](https://drive.google.com/file/d/1D9DoIqTtTtV3AuaCSj20b5o7ftXE2KAk/view?usp=sharing)|2|0:none,1:hate|
|[BEEP only, 2stage, offensive](https://drive.google.com/file/d/1CqG5jQfF0FUKMbIhhdX6HtziIngmgAJJ/view?usp=sharing)|2|0:none,1:offensive|
|[Whole data, 2stage, hate](https://drive.google.com/file/d/1CoChY-cpi3hTe_N-triUI07PDuPHk5JF/view?usp=sharing)|2|0:none,1:hate|
|[Whole data, 2stage, hate](https://drive.google.com/file/d/1UOuqedLA8fbEXL1JbSw17ZttF1aUXidj/view?usp=sharing)|2|0:none,1:offensive|

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
- 악플 분석 모델  
  - Kaggle 대회 Test set 기준 
  - 2-STAGE 모델 적용 전 : f1-score 0.628
  - 2-STAGE 모델 적용 후 : f1-score 0.648
  - [Kaggle 리더보드](https://www.kaggle.com/c/korean-hate-speech-detection/leaderboard)
  - Best 3 model 
    ![Validation Score](https://user-images.githubusercontent.com/42054789/147218458-a64e0450-60b3-43c0-9a37-33eeadf7ce1f.png)

- 감성 분석 모델
  - 라이브 커머스 데이터 기준
  - 액티브 러닝 적용 전 : accuracy 0.64
  - 액티브 러닝 적용 후 : accuracy 0.95 

# Reference

## Paper

- [ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555)

- [Don't Stop Pretraining: Adapt Language Models to Domains and Tasks](https://arxiv.org/abs/2004.10964)

- [Curriculum Learning for Natural Language Understanding](https://aclanthology.org/2020.acl-main.542.pdf)

- [BEEP! Korean Corpus of Online News Comments for Toxic Speech Detection](https://arxiv.org/abs/2005.12503)


- [Learning Loss for Active Learning
](https://arxiv.org/abs/1905.03677)
