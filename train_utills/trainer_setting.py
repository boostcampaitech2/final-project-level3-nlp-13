from typing import *

from transformers import Trainer, TrainingArguments

def set_trainer(
        config: Dict, 
        model, # hugging face or custom 모델 
        train_dataset, # torch.nn.Dataset
        valid_dataset # torch.nn.Dataset
    ):
    '''
        arguments
            config : str
                실험 설정을 위한 하이퍼파라미터 값들
            model : str
                hugging face or custom 모델 
            train_dataset, valid_dataset : torch.nn.Dataset
                학습 및 검증에 사용할 데이터 셋

        return
            AutoTokenizer

        summary
            토크나이저의 이름과 타입에 따라 학습 및 추론에 사용할 모델 반환
    '''
    training_args = TrainingArguments(   
        report_to=['wandb'],
        output_dir=config['output']['model_save_dir'],
        save_total_limit=config['train']['save_total_limit'],
        num_train_epochs=config['train']['epochs'],
        learning_rate=config['train']['learning_rate'],
        per_device_train_batch_size=config['train']['train_batch_size'],
        per_device_eval_batch_size=config['train']['eval_batch_size'],
        warmup_steps=config['train']['warm_up_step'],
        weight_decay=config['train']['weight_decay'],        
        save_strategy=config['train']['save_strategy'],     
        evaluation_strategy=config['train']['evaluation_strategy'],               
        load_best_model_at_end=config['train']['load_best_model_at_end'],
        run_name=config['wandb']['run_name']
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
    )

    return trainer