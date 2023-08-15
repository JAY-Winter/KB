# 
from module.DOC import *
from module.KOBART import summary_KOBART
from module.DOC2VEC import *
from module.SEARCH import *
#
from starlette.requests import Request
from fastapi import FastAPI, File, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, HTTPException, Form, Depends
#
from kobart_transformers import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration
#
import openai
from io import BytesIO
from transformers import pipeline

# Fast 서버 구동
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# 유사도 검색 시 업로드 파일과 유사도를 비교할 폴더 경로
SEARCH_DIRECTORY_PATH = os.getenv('SEARCH_DIRECTORY_PATH', default='')

# KOBART 모델 로딩
model = BartForConditionalGeneration.from_pretrained('/Users/heyon/Desktop/v3')
tokenizer = get_kobart_tokenizer()

def load_model():
    '''
    KO-BART 객체 반환
    '''
    return model


def load_tokenizer():
    '''
    KO-BART Tokenizer 반환
    '''
    return tokenizer


##########################################
#               End-Point                #
##########################################
@app.get('/')
async def render_main(request: Request):
    '''
    Main Page 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/template/similarity_files')
async def render_search_similiary_files(request: Request):
    '''
    유사 파일 검색 페이지 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('upload.html', {'request': request})


@app.get('/template/keyword_files')
async def render_search_similarity_files(request: Request):
    '''
    키워드 기준 유사 파일 검색 페이지 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('search.html', {'request': request})


@app.post('/summary/')
async def summarize_docx(file: UploadFile = File(...), model: BartForConditionalGeneration = Depends(load_model), tokenizer = Depends(load_tokenizer)):
    ''' 
    업로드한 파일을 요약 및 유사한 파일과 비교하는 API 입니다.
    '''
    if file.filename.endswith('.docx'):
        file_contents = await file.read()
        document = read_docx(BytesIO(file_contents))    
    elif file.filename.endswith('.txt'):
        file_contents = await file.read()
        document = file_contents.decode('utf-8')
    else:
        raise HTTPException(status_code=400, detail='Invalid file type')

    # TF-IDF 를 통한 유사 파일 검색
    file_type = file.filename.split('.')[-1]
    similar_documents = await compare_similarity(document, file_type, SEARCH_DIRECTORY_PATH)
    
    # KOBART 요약
    kobart_summary = summary_KOBART(document, model, tokenizer)

    # 유사도 비교 : 업로드된 파일과 로컬에 저장된 파일들 사이의 유사도를 비교하여 정렬된 파일 리스트를 가져옵니다.       
    return {'kobart_summary': kobart_summary, 'similar_documents': similar_documents}


@app.get('/file/')
def get_file(path):
    '''
    유사한 파일 다운로드 API 입니다.
    '''
    return FileResponse(path, filename=path)


@app.post('/summary_by_path/')
async def summary_by_path(path: str = Form(...), model: BartForConditionalGeneration = Depends(load_model), tokenizer = Depends(load_tokenizer)):
    '''
    유사한 파일 요약 API 입니다.
    '''
    # 파일 경로에서 실제 문서 읽기
    document_path = os.path.join(os.getcwd(), path)
    document = await read_file_from_path(document_path)
    
    kobart_summary = summary_KOBART(document, model, tokenizer)
    return {'kobart_summary': kobart_summary}

    
@app.get('/search/keyword')
def search_keyword(keyword):
    if not keyword:
        return HTTPException(status_code=400, detail= '키워드가 제공되지 않았습니다.')

    # 유사한 문서를 가져오는 함수를 사용
    results = recommend_docs_TF_IDF(keyword)

    # 결과를 JSON 형식으로 반환
    return {'results' : results}