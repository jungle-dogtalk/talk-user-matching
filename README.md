# 아나콘다 설치 및 가상 환경 설정

## 아나콘다 설치 
[아나콘다 다운로드](https://www.anaconda.com/download/success) 페이지에 접속하여 아나콘다 설치 파일을 다운로드하고 설치

## 가상 환경 만들기
아나콘다가 설치된 후, 아래 명령어를 사용하여 `dogtalk`라는 이름의 가상 환경을 만듦

```
conda create --name dogtalk python=3.8
```

## 패키지 설치
```
pip install -r requirements.txt

conda install numpy pandas

pip install gensim==3.8.3
```

-------

# Docker 이미지 빌드 및 컨테이너 실행

## Docker 이미지 빌드
프로젝트 디렉토리에서 다음 명령어를 사용하여 `dogtalk`라는 이름의 Docker 이미지를 빌드

```
docker build -t dogtalk .
```


##  Docker 컨테이너 실행 명령어
다음 명령어를 사용하여 dogtalk 이미지를 기반으로 하는 컨테이너를 실행
이 컨테이너는 백그라운드에서 실행되며, 호스트의 포트 6000을 컨테이너의 포트 6000에 매핑함
```
docker run -d -p 6000:6000 dogtalk
```
