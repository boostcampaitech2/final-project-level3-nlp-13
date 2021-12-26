# 호스트, 넌 방송만해! 관리는 우리가 할께!

- 🍀 Naver Boost camp AI tech 2nd final project
- 📹 [Demonstration video]() , 🖇️ [presentation slide](https://docs.google.com/presentation/d/1pmBbn0NuesvNO-vzAuRdGg0Ph0q09odh/edit?usp=sharing&ouid=116368231704837867107&rtpof=true&sd=true)

## 1.Project Abstract

### 프로젝트 개요

* 목적
    * 라이브 커머스를 진행하는 호스트를 위한 실시간 채팅 매니지먼트(a.k.a CLUE 매니지먼트)

* 주요 기능
    * 악성채팅(욕설, 비방, 혐오발언 등)에 대한 대체 문구 처리
    * 악성채팅과 부정적인 반응 / FAQ 성 채팅글을 따로 확인할 수 있는 리스트 제공
    * 채팅글을 바탕으로한 실시간 시청자 반응 대시보드 구현




### Team CLUE 

👉 _"Create Life Until End of day"_

#### 👨‍👩‍👦‍👦 Members  

김강민|김동현|김상욱|양준혁|이종혁|임경현|임효석|
:-:|:-:|:-:|:-:|:-:|:-:|:-:
<img src='https://user-images.githubusercontent.com/76195885/147217034-9a262d4e-d80a-4d57-a9b9-fb25157e77c9.jpeg' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147217030-8a534d71-5c65-420b-8421-c884d6f1a1e4.jpeg' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147217018-73057671-eee5-4efb-850b-3af6951fdf04.jpeg' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147216867-4ffcb585-9740-48c2-838a-f1eeb3908d65.jpeg' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147216683-59af4388-43c9-4f9a-ad23-6384233a94f3.JPG' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147216609-0fcfe0f8-a5a9-4047-8344-6cce845bc6bd.jpeg' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/76195885/147216489-85773d7f-cfa7-4f59-b418-f871aa20deae.png' height=80 width=80px></img>
[Github](https://github.com/Gangsss)|[Github](https://github.com/Kimdongui)|[Github](https://github.com/lswkim)|[Github](https://github.com/surfing2003)|[Github](https://github.com/jonhyuk0922)|[Github](https://github.com/KyungHyunLim)|[Github](https://github.com/limhyoseok)

#### 🏆 Contribution  

- [`임경현`](https://github.com/KyungHyunLim) &nbsp; PM • Baseline • Hate speech detection model • Backend
- [`김강민`](https://github.com/Gangsss) &nbsp; Hate speech detection model • Refactoring
- [`김동현`](https://github.com/Kimdongui) &nbsp; Hate speech detection model • Refactoring • Frontend
- [`김상욱`](https://github.com/lswkim) &nbsp; Frontend • Sentiment analysis model
- [`양준혁`](https://github.com/surfing2003) &nbsp; Sentiment analysis model • Post-processing
- [`이종혁`](https://github.com/jonhyuk0922) &nbsp; Presentation • Sentiment analysis model
- [`임효석`](https://github.com/limhyoseok) &nbsp; Active learning • Web crawling • Prototype


## 2.Dependency management

👉 Poetry를 통한 패키지 버전 관리 

```
# curl 설치
apt-get install curl #7.58.0

# poetry 설치
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# poetry 탭완성 활성화
~/.bashrc를 수정하여 poetry를 shell에서 사용 할 수 있도록 가상환경에 추가
poetry use [사용하는 가상환경의 `python path` | 가상환경이 실행중이라면 `python`]  

# repo download 후 버전 적용 (poetry.toml에 따라 적용)
poetry install
```


## 3. Equipment & Software

- [OS] Linux version 4.4.0-59-generic
- [CPU / GPU] Intel(R) Xeon(R) Gold 5220 CPU @ 2.20GHz / Tesla V100-SXM2-32GB  * 7
- [Collaboration Tool] Git-hub / Poetry / Slack / Notion / Wandb 
- [IDE] VSCode / Pycharm / Jupyter lab


## 4.시연 영상
![최종플젝 시연](https://user-images.githubusercontent.com/59302419/147213596-a13b3f6f-ae44-496b-a5a8-cdf8f9f9822d.gif)


## 5. License

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />
