import os
from docx import Document
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def read_docx(file):
    doc = Document(file)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs)


def read_docx_from_path(path: str):
    '''주어진 경로에서 DOCX 파일을 읽어 텍스트를 반환합니다.'''
    try:
        doc = Document(path)
        return [p.text for p in doc.paragraphs if p.text.strip() != '']
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def docx_to_text(file_path):
    doc = Document(file_path)
    return ' '.join(paragraph.text for paragraph in doc.paragraphs)


def get_all_docx_files_in_directory(directory_path):
    '''
    주어진 디렉토리 내의 모든 .docx 파일의 경로를 리스트로 반환합니다.
    '''
    return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.docx')]


def compare_similarity(uploaded_file_content):
    '''
    업로드한 파일과 로컬 파일의 유사도를 비교합니다.
    '''
    # 로컬에 저장된 문서들을 로드합니다.
    file_paths = get_all_docx_files_in_directory('/Users/heyon/Desktop/KB/file')
    documents = [docx_to_text(file_path) for file_path in file_paths]

    # 업로드된 파일의 내용도 리스트에 추가합니다.
    documents.append(uploaded_file_content)

    # TfidfVectorizer를 사용하여 문서들을 벡터화합니다.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 마지막 문서 (업로드된 문서)와 나머지 문서들의 유사도를 계산합니다.
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # 유사도와 파일 경로를 결합하고 유사도 순으로 정렬합니다.
    sorted_files = sorted(zip(similarities[0], file_paths), key=lambda x: x[0], reverse=True)

    # 정렬된 파일 경로를 반환합니다.
    return [file for file in sorted_files]

