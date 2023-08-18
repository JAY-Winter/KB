FROM python:3.9

# git 설치
RUN apt-get update && apt-get install -y git && apt-get install -y unzip

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install uvicorn
RUN pip install aiofiles
RUN pip install python-docx
RUN pip install fastapi
RUN pip install scikit-learn
RUN pip install torch
RUN pip install kobart_transformers
RUN pip install transformers
RUN pip install python-multipart
RUN pip install redis


# GitHub 저장소 다운로드
WORKDIR /app
RUN git clone https://github.com/JAY-Winter/KB.git

# 테스트 파일 압축해제
WORKDIR /app/KB
RUN unzip file.zip

# Ko-BART 모델 다운로드 및 압축 해제
WORKDIR /app/KB
RUN wget https://github.com/JAY-Winter/KB/raw/main/ko-bart.zip?download=
RUN unzip 'ko-bart.zip?download='

# FastAPP 서버 구동
WORKDIR /app/KB/backend
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]