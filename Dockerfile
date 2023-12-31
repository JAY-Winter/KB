# 기본 이미지 설정
FROM python:3.9

RUN apt-get update && apt-get install -y git unzip && \
    pip install --upgrade pip && \
    pip install uvicorn aiofiles python-docx fastapi scikit-learn torch kobart_transformers transformers python-multipart redis

# GitHub 저장소 다운로드
WORKDIR /app
RUN git clone https://github.com/JAY-Winter/KB.git

# 테스트 파일 압축해제
WORKDIR /app/KB
RUN unzip file.zip
RUN rm -rf file.zip

# Ko-BART 모델 다운로드 및 압축 해제
WORKDIR /app/KB
RUN wget https://github.com/JAY-Winter/KB/raw/main/ko-bart.zip?download=
RUN unzip 'ko-bart.zip?download='
RUN rm -rf ko-bart.zip
RUN rm -rf 'ko-bart.zip?download='

# FastAPP 서버 구동
WORKDIR /app/KB/backend
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]