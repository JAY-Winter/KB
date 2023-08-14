import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

model = Doc2Vec.load('/Users/heyon/Desktop/KB/test/test_model.model')

def txt_to_text(file_path) -> list[str]:
    '''
    txt 파일을 text: [list] 로 분리
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        content = [file.read()]
    return content


def infer_file(file):
    inferred_v = model.infer_vector(file)
    return inferred_v


def compare_similarity_doc2vec(inferred_v):
    most_similar_docs = model.docvecs.most_similar([inferred_v], topn=5)
    return most_similar_docs