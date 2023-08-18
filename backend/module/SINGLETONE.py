from module.DOC import *
#
from kobart_transformers import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration
#
from sklearn.feature_extraction.text import TfidfVectorizer

#
import os

class Main():

    def __init__(self):

        # 유사도 검색 시 업로드 파일과 유사도를 비교할 폴더 경로
        self.SEARCH_DIRECTORY_PATH = os.getenv('SEARCH_DIRECTORY_PATH', default='')

        # KOBART 모델 로딩
        self.KOBART_MODEL_PATH = os.getenv('KOBART_MODEL_PATH', default='')
        self.model = BartForConditionalGeneration.from_pretrained(self.KOBART_MODEL_PATH)
        self.tokenizer = get_kobart_tokenizer()    
        
        # 검색 폴더 내 문서 변수화
        self.documents = []
        self.all_files = []

        txt_files = get_all_files_in_directory(self.SEARCH_DIRECTORY_PATH, 'txt')
        docx_files = get_all_files_in_directory(self.SEARCH_DIRECTORY_PATH, 'docx')
        
        self.all_files += txt_files
        self.all_files += docx_files

        # documents 리스트에 파일의 내용과 파일 경로를 함께 저장합니다.
        self.documents += [(txt_to_text(file_path), file_path) for file_path in txt_files]
        self.documents += [(docx_to_text(file_path), file_path) for file_path in docx_files]

        # SEARCH_DIRECTORY 내 문서 TF-IDF
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform([doc_file[0] for doc_file in self.documents])


    def load_model(self):
        '''
        KO-BART 객체 반환
        '''
        return self.model


    def load_tokenizer(self):
        '''
        KO-BART Tokenizer 반환
        '''
        return self.tokenizer


    def get_SEARCH_DIRECTORY_PATH(self):
        return self.SEARCH_DIRECTORY_PATH


    def get_vectorizer(self):
        return self.vectorizer


    def get_tfidf_matrix(self):
        return self.tfidf_matrix


    def get_documents(self):
        return self.documents


    def get_all_files(self):
        return self.all_files


class MainInstance():
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Main()
        return cls._instance