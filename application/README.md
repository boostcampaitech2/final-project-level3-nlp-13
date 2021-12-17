# final-project-level3-nlp-13
final-project-level3-nlp-13 created by GitHub Classroom

## Info
- 기본적인 웹통신 구조 샘플입니다. 아래 Reference를 혼합하여 구현하였으며, Model, Service등의 구조는 편한대로 사용하여도 될 것 같습니다. 
- 부트스트랩에 불필요한 라이브러리가 포함되어있어 용량이 다소 큽니다. (부트스트랩 레퍼런스 사이트 참고하여 추가로 사용할 UI 정하고 정리하면 좋을 것 같습니다.)
- 모니터 비율에 따라 chat 페이지 UI가 깨질 수 있습니다.(프론트앤드 너무 힘듬...)

## Install
```
requests = "2.26.0"
fastapi = "0.70.0"
uvicorn = "0.15.0"
python-dotenv = "0.19.1"
aiofiles = "0.7.0"
python-multipart = "0.0.5"
Jinja2 = "3.0.2"
Markdown = "3.3.4"
pytest = "6.2.5"
loguru = "^0.5.3"
```

## Run Server
application 경로에서 아래 명령어 수행
```
python -m app
```

## Webbrowser
```
https://localhost:8080/
https://localhost:8080/sample/
https://localhost:8080/chat/
```

## Directory
```
application
├── app
│   ├── core (not used)     - application configuration, startup events, logging.
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── events.py
│   │   └── logging.py
│   ├── models (not used)   - pydantic models for this application.
│   │   └── prediction.py
│   ├── routers             - api routers
│   │   ├── chat.py
│   │   └── sample.py
│   ├── services (not used) - logic that is not just crud related.
│   │   └── predict.py
│   └── main.py
├── files                   - storage for chatting log files
├── statics                 - static files such as css, image, js
└── templates               - html template
```
## Reference
### fastapi code
https://github.com/arthurhenrique/cookiecutter-fastapi/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D
https://github.com/shinokada/fastapi-web-starter
### bootstrap code
https://github.com/zuramai/mazer