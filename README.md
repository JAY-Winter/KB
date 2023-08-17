# KB financial 공모전
**유사문서 검색 및 요약 서비스**

⇒ 기존 작성되어 있는 행내 각종 품의문, 시행문을 원하는 내용 키워드 검색 또는 파일 업로드를 통해

**가장 적합한 문서를 찾는 검색 AI**

⇒ 본부부서에서 각종 시행문, 품의문 작성 시 기존에 작성했던 유사한 문서를 참고하는 경우가 많기 때문에 원하는 양식을 AI가 인식하여 쉽게 검색할 수 있다면 업무시간 단축이 가능할 것으로 생각함 검색 키워드에 맞는 각종 품의문이나 시행문을 가장 조회수가 높거나 저장횟수가 많은 것부터 나열하는 등으로 중요도를 AI가 판정하여 제시해준다면 문서탐색시간을 줄일 수 있을 것으로 생각함

---

# EXPORT

## 0. 도커 다운로드

1. https://www.docker.com/ 방문하여 현재 환경에 맞는 파일 다운로드 및 실행

## 1. 도커 컨테이너 구동

```
docker run -itd \
--name kb-fast \
-p 8000:8000 \
-e SEARCH_DIRECTORY_PATH='/app/KB/file' \
-e KOBART_MODEL_PATH='/app/KB/ko-bart' \
rubat0/kb-fast-app
```

1. `rubat0/kb-fast-app` : 배포 도커 이미지를 활용하여 컨테이너 구동
2. `-e SEARCH_DIRECTORY_PATH` : 파일 유사도 검색 시, 조회할 폴더 경로 환경변수 지정
3. `-e KOBART_MODEL_PATH` : 파일 요약 시, 사용할 KO-BART 모델 경로 환경변수 지정

---

# TEST

## 1. 키워드 별 유사한 파일 찾기

1. http://127.0.0.1:8000/ 방문
2. ![image-20230817162852110](/Users/heyon/Desktop/KB/assets/image-20230817162852110.png) 

**키워드로 비슷한 파일 찾기** 클릭

3. 키워드 입력

![image-20230817162933617](/Users/heyon/Desktop/KB/assets/image-20230817162933617.png)

- 해당 키워드와 유사한 파일 상위 5개 추천

4. 파일 다운로드

## 2. 업로드 파일과 유사한 파일 찾기

1. ![image-20230817162852110](/Users/heyon/Desktop/KB/assets/image-20230817162852110.png)

**업로드해서 비슷한 파일 찾기** 클릭

2. 파일 업로드 및 Upload 버튼 클릭

3. 업로드한 파일과 유사한 파일 상위 10개 추천

   - 유사한 파일 요약 시, 비동기 처리로 우선 요약 처리된 파일부터 렌더링

   ![image-20230817163123588](/Users/heyon/Desktop/KB/assets/image-20230817163123588.png)

4. 파일 다운로드 및 확인
