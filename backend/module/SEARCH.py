import os
from pprint import pprint

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from sklearn.cluster import DBSCAN
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.cluster import KMeans
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def get_all_txt_files_in_directory(directory_path):
    '''
    주어진 디렉토리 내의 모든 .txt 파일의 경로를 리스트로 반환합니다.
    '''
    return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.txt')]

def txt_to_text(file_path):
    '''
    주어진 .txt 파일의 내용을 문자열로 반환합니다.
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


directory_path = '/Users/heyon/Desktop/KB/test/docs' 
all_txt_file_paths = get_all_txt_files_in_directory(directory_path)

# documents 리스트에 파일의 내용과 파일 경로를 함께 저장합니다.
documents = [(txt_to_text(file_path), directory_path+file_path) for file_path in all_txt_file_paths]

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()

# 파일의 내용만을 사용하여 TF-IDF 벡터화를 수행합니다.
tfidf_matrix = vectorizer.fit_transform([doc[0] for doc in documents])

# 새로운 키워드에 대한 유사도 계산
def recommend_docs_TF_IDF(keyword):
    keyword_vector = vectorizer.transform([keyword])

    # 키워드와 각 문서 사이의 코사인 유사도 계산
    cosine_similarities = cosine_similarity(keyword_vector, tfidf_matrix).flatten()

    # 상위 5개 유사도 인덱스
    most_similar_indices = cosine_similarities.argsort()[-5:][::-1]

    # 추천된 문서, 그 문서의 유사도 값, 파일명을 반환
    recommended_docs_with_scores = sorted([(documents[i][0], cosine_similarities[i], os.path.basename(documents[i][1])) for i in most_similar_indices], key=lambda item: -item[1]) 
    return recommended_docs_with_scores
