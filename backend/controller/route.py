from module.SINGLETONE import MainInstance
from module.DOC import *
from module.SEARCH import *
from module.KOBART import summary_KOBART
from module.SINGLETONE import MainInstance as MainInstance
#
from fastapi import APIRouter
from starlette.requests import Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, HTTPException, Form, Depends, File, HTTPException
#
from transformers.models.bart import BartForConditionalGeneration
#
from io import BytesIO


# Router 설정
router = APIRouter()

# template 설정
templates = Jinja2Templates(directory='templates')


@router.get('/')
async def render_main(request: Request):
    '''
    Main Page 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('main.html', {'request': request})


@router.get('/template/similarity_files')
async def render_search_similiary_files(request: Request):
    '''
    유사 파일 검색 페이지 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('upload.html', {'request': request})


@router.get('/template/keyword_files')
async def render_search_similarity_files(request: Request):
    '''
    키워드 기준 유사 파일 검색 페이지 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('search.html', {'request': request})


@router.post('/summary/')
async def summarize_docx(file: UploadFile = File(...), model: BartForConditionalGeneration = Depends(MainInstance.get_instance().load_model), tokenizer = Depends(MainInstance.get_instance().load_tokenizer)):
    ''' 
    업로드한 파일을 요약 및 유사한 파일과 비교하는 API 입니다.
    '''
    if file.filename.endswith('.docx'):
        file_contents = await file.read()
        uploaded_file_content = read_docx(BytesIO(file_contents))    
    elif file.filename.endswith('.txt'):
        file_contents = await file.read()
        uploaded_file_content = file_contents.decode('utf-8')
    else:
        raise HTTPException(status_code=400, detail='Invalid file type')
    
    # TF-IDF 를 통한 유사 파일 검색
    file_type = file.filename.split('.')[-1]
    uploaded_file_name = file.filename
    similar_documents = await compare_similarity(uploaded_file_name ,uploaded_file_content, file_type, MainInstance.get_instance().get_SEARCH_DIRECTORY_PATH())
    
    # KOBART 요약
    kobart_summary = summary_KOBART(uploaded_file_content, model, tokenizer)

    # 유사도 비교 : 업로드된 파일과 로컬에 저장된 파일들 사이의 유사도를 비교하여 정렬된 파일 리스트를 가져옵니다.       
    return {'kobart_summary': kobart_summary, 'similar_documents': similar_documents}


@router.post('/summary_by_path/')
async def summary_by_path(path: str = Form(...), model: BartForConditionalGeneration = Depends(MainInstance.get_instance().load_model), tokenizer = Depends(MainInstance.get_instance().load_tokenizer)):
    '''
    유사한 파일 요약 API 입니다.
    '''
    from main import Redis_Instance
    from main import MainInstance as MainInstance

    # Redis 를 활용한 Cache 적용
    redis_client = Redis_Instance.redis_client
    SEARCH_DIRECTORY_PATH = MainInstance.get_instance().get_SEARCH_DIRECTORY_PATH()
    hash_key = 'summaryAPI' +  SEARCH_DIRECTORY_PATH + '/' + path

    cached_result = redis_client.get(hash_key)
    if cached_result:
        return eval(cached_result.decode('utf-8'))
    else:
        # 파일 경로에서 실제 문서 읽기
        document = await read_file_from_path(path)  
        
        kobart_summary = summary_KOBART(document, model, tokenizer)

        results = {'kobart_summary': kobart_summary}
        redis_client.set(hash_key, str(results), ex=3600)
        return results

    
@router.get('/search/keyword')
def search_keyword(keyword):
    if not keyword:
        return HTTPException(status_code=400, detail= '키워드가 제공되지 않았습니다.')

    # 유사한 문서를 가져오는 함수를 사용
    results = recommend_docs_TF_IDF(keyword)

    # 결과를 JSON 형식으로 반환
    return {'results' : results}


@router.get('/file/')
def get_file(path):
    '''
    유사한 파일 다운로드 API 입니다.
    '''
    filename = os.path.basename(path)
    return FileResponse(path, filename=filename)