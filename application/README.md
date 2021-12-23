## 1. 웹서버 실행
👉 application 디렉토리 경로에서 아래 명령어 수행
```
python -m app
```

## 2. 데모 페이지 접속 URL
```
https://{localhost}:8080/chat/
```

## 3. 🏗️ 프로젝트 구조
### 3-1. 저장소 구조
```
application
├── app
│   ├── models
│   │   ├── model.py           - load model, tokenizer / inference
│   │   └── weights
│   │       ├── beep_best.bin  - hate speech detection model(need to upload)
│   │       └── senti_best.bin - sentiment analysis model(need to upload)
│   ├── routers                - api routers
│   │   ├── chat.py            - router of demo service
│   │   └── sample.py
│   ├── services            
│   │   └── predict.py         - rule-based classification / word-cloud dataset
│   └── main.py
├── files                      - storage for chatting log files
├── statics                    - static files such as css, image, js
└── templates                  - html template
```
## 4. Reference
### 👉 fastapi code  
https://github.com/arthurhenrique/cookiecutter-fastapi/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D  
https://github.com/shinokada/fastapi-web-starter  
### 👉 bootstrap code  
https://github.com/zuramai/mazer
### 👉 chart library  
https://apexcharts.com  
https://www.anychart.com/

