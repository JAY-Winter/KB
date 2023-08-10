# 
from module.DOC import *
from module.KOBART import summary_KOBART
#
from starlette.requests import Request
from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, HTTPException, Form, Depends
#
import openai
from io import BytesIO
from transformers import pipeline

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


##########################################
#               End-Point                #
##########################################
@app.get('/')
async def render_main(request: Request):
    '''
    Main Page 렌더링 API 입니다.
    '''
    return templates.TemplateResponse('upload.html', {'request': request})


@app.post('/summary/')
async def summarize_docx(file: UploadFile = File(...)):
    ''' 
    업로드한 파일을 요약 및 유사한 파일과 비교하는 API 입니다.
    '''
    if file.filename.endswith('.docx'):
        file_contents = await file.read()
        document = read_docx(BytesIO(file_contents))

        # KOBART 요약
        kobart_summary = summary_KOBART(document)

        # 유사도 비교        
        # 업로드된 파일과 로컬에 저장된 파일들 사이의 유사도를 비교하여 정렬된 파일 리스트를 가져옵니다.
        similar_documents = compare_similarity(document)

        # 최종 결과 반환
        return {'kobart_summary': kobart_summary, 'similar_documents': similar_documents}
    else:
        raise HTTPException(status_code=400, detail='Invalid file type')


@app.get('/file/')
def get_file(path):
    '''
    유사한 파일 다운로드 API 입니다.
    '''
    return FileResponse(path, filename=path)


@app.post('/summary_by_path/')
async def summary_by_path(path: str = Form(...)):
    '''
    유사한 파일 요약 API 입니다.
    '''
    # 파일 경로에서 실제 문서 읽기
    document_path = os.path.join(os.getcwd(), path)
    document = '\n'.join(read_docx_from_path(document_path))

    kobart_summary = summary_KOBART(document)
    return {'kobart_summary': kobart_summary}


##########################################
#               Module                   #
##########################################
