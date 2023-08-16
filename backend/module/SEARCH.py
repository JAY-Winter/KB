from module.SINGLETONE import MainInstance as MainInstance
#
from sklearn.metrics.pairwise import cosine_similarity
#
import os


def recommend_docs_TF_IDF(keyword):
    '''
    입력받은 키워드에 대한 유사한 파일 검색 API 입니다.
    '''
    documents = MainInstance.get_instance().get_documents()
    vectorizer = MainInstance.get_instance().get_vectorizer()
    tfidf_matrix = MainInstance.get_instance().get_tfidf_matrix()
    keyword_vector = vectorizer.transform([keyword])

    # 키워드와 각 문서 사이의 코사인 유사도 계산
    cosine_similarities = cosine_similarity(keyword_vector, tfidf_matrix).flatten()

    # 상위 5개 유사도 인덱스
    most_similar_indices = cosine_similarities.argsort()[-5:][::-1]

    # 추천된 문서, 그 문서의 유사도 값, 파일명을 반환
    recommended_docs_with_scores = sorted([(documents[i][0], cosine_similarities[i], os.path.basename(documents[i][1])) for i in most_similar_indices], key=lambda item: -item[1]) 
    return recommended_docs_with_scores