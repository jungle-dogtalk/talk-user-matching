# Dockerfile
FROM continuumio/miniconda3

# 작업 디렉토리 설정
WORKDIR /app

# 환경 파일과 애플리케이션 파일 복사
COPY requirements.txt /app/
COPY ./app /app/

# Conda 및 pip 패키지 설치
RUN conda install -y python=3.8 numpy pandas && \
    pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 6000

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000"]