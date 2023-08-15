import os
import aiofiles
from pprint import pprint
from docx import Document
from fastapi import HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def read_docx(file_path: str) -> str:
    '''
    주어진 경로의 .docx 파일 내용을 문자열로 반환합니다.
    '''
    doc = Document(file_path)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip() != '')


def docx_to_text(file_path):
    doc = Document(file_path)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs)


async def read_file_from_path(path: str) -> str:
    '''
    주어진 경로에서 파일을 읽어 텍스트를 반환합니다.
    '''
    try:
        if path.endswith('.docx'):
            return read_docx(path)
        if path.endswith('.txt'):
            async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
                return await f.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_all_files_in_directory(directory_path, file_type):
    '''
    주어진 디렉토리 내의 파일 타입별 모든 파일의 경로를 리스트로 반환합니다.
    '''
    if file_type == 'docx':
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.docx')]
    elif file_type == 'txt':
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.txt')]


async def compare_similarity(uploaded_file_content, file_type, search_directory_path):
    '''
    업로드한 파일과 로컬 파일의 유사도를 비교합니다.
    '''
    all_files = get_all_files_in_directory(search_directory_path, file_type)

    if file_type == 'docx':
        documents = [docx_to_text(file_path) for file_path in all_files]
    elif file_type == 'txt':
        documents = [await read_file_from_path(txt_file) for txt_file in all_files]

    # 업로드된 파일의 내용도 리스트에 추가합니다.
    documents.append(uploaded_file_content)

    # TfidfVectorizer를 사용하여 문서들을 벡터화합니다.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 마지막 문서 (업로드된 문서)와 나머지 문서들의 유사도를 계산합니다.
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # 유사도와 파일 경로를 결합하고 유사도 순으로 정렬합니다.
    sorted_files = sorted(zip(similarities[0], all_files), key=lambda x: x[0], reverse=True)

    # 정렬된 파일 경로를 반환합니다.
    return [file for file in sorted_files[:10]]