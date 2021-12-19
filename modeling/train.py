import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import sys
import getopt

from utills.utill import read_config
from models.utill import get_model, get_tokenizer
from train_utills.trainer_setting import set_trainer
from train_utills.test import do_test
from data.dataset import DatasetForHateSpeech

from logger.mylogger import set_logger

def get_config(loger):
    '''
        arguments
            loger
                로깅을 위한 객체

        summary
            config.json을 읽어와서 반환
    '''
    argv = sys.argv
    file_name = argv[0] # 실행시키는 파일명
    config_path = ""   # config file 경로

    try:
        # 파일명 이후 부터 입력 받는 옵션
        # help, config_path
        opts, etc_args = getopt.getopt(argv[1:], "hc:", ["help", "config_path="])
    except getopt.GetoptError:
        # 잘못된 옵션을 입력하는 경우
        loger.error(f"wrong config path, please follow -> {file_name} -c <config_path>")
        sys.exit(2)
        
    # 입력된 옵션을 적절히 변수로 입력
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            loger.info(f"{file_name} HELP: -c <config_path>")
            sys.exit(0)
        elif opt in ("-c", "--config_path"):
            config_path = arg
    
    # 입력이 필수적인 옵션 입력이 없으면 오류 메시지 출력
    if len(config_path) < 1:
        loger.error(f"{file_name} -c <config_path> is madatory")
        sys.exit(2)

    config = read_config(config_path)
    return config

if __name__=='__main__':
    # 1. 실험 환경 변수 읽어 오기
    loger = set_logger()
    config = get_config(loger)

        # logging for currnet infom
    loger.info('model name: ' + config['model']['model_name'])
    loger.info('tokenizer name: ' + config['tokenizer']['tokenizer_name'])
    loger.info('wandb run_name: ' + config['wandb']['run_name'])

    # 2. 토크나이저 불러오기
    loger.info("Load tokenizer")
    tokenizer = get_tokenizer(
        tokenizer_name=config['tokenizer']['tokenizer_name'], 
        tokenizer_type=config['tokenizer']['tokenizer_type']
    )
    loger.info("Load tokenizer Completed")

    # 3. 모델 및 옵티마이저 불러오기
    loger.info("Load model")
    model = get_model(
        model_name=config['model']['model_name'], 
        model_type=config['model']['model_type'],
        num_classes=config['model']['num_classes']
    )
    model.resize_token_embeddings(len(tokenizer))
    loger.info("Load model Completed")

    if config['train']['do_train']:
        # 4. 학습 및 검증을 위한 데이터 준비
        loger.info("Make dataset")
        train_dataset = DatasetForHateSpeech(
                type = 'train', 
                tokenizer = tokenizer,
                config = config,
                path =  config['data']['train_data_path'],
                version = config['data']['train_data_version']
            )
        loger.info("Make dataset completed (Train)")
        valid_dataset = DatasetForHateSpeech(
                type = 'valid', 
                tokenizer = tokenizer,
                config = config,
                path =  config['data']['valid_data_path'],
                version = config['data']['valid_data_version']
            )
        loger.info("Make dataset completed (Valid)")
        
        # 5. 모델 학습하기
        loger.info("Set trainer")
        trainer = set_trainer(config, model, train_dataset, valid_dataset)

        # 6. 학습
        loger.info("Start train")
        trainer.train()

    # 7. 평가 (use testset)
    if config['test']['do_test']:
        loger.info("Start test!!")
        test_dataset = DatasetForHateSpeech(
                type = 'test', 
                tokenizer = tokenizer,
                config = config,
                path =  config['data']['test_data_path'],
                version = config['data']['test_data_version']
            )
        loger.info("Make dataset completed (Test)")

        result = do_test(config, model, test_dataset)
        loger.info(f"f1-score: {result['f1-score']} | accuracy: {result['accuracy']} | runtime: {result['time']['runtime']}")

