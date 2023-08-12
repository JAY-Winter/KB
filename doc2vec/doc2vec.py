from pprint import pprint
from docx import Document
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument




def txt_to_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = [file.read()]
    return content


def get_all_txt_files_in_directory(directory_path):
    '''
    주어진 디렉토리 내의 모든 .txt 파일의 경로를 리스트로 반환합니다.
    '''
    return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.txt')]



all_txt_file_path = get_all_txt_files_in_directory('/Users/heyon/Desktop/KB/test/docs')

docs = []
for doc in all_txt_file_path:
    _doc = txt_to_text(doc)
    docs.append(_doc)


common_texts_and_tags = [
    (text, [f'str_{i}',]) for i, text in enumerate(docs)
]

# pprint(common_texts_and_tags)
TRAIN_documents = [TaggedDocument(words=text, tags=tags) for text, tags in common_texts_and_tags]


# 여러 Parameter들을 사용하여 튜닝할 수 있음. 
model = Doc2Vec(TRAIN_documents, vector_size=5, window=3, epochs=40, min_count=0, workers=4)

# 위 학습을 통해 생성된 model
model.save('./new_test_model.model')

for text, tags in common_texts_and_tags:
    trained_doc_vec = model.docvecs[tags[0]]
    inferred_doc_vec = model.infer_vector(text)
    
    # 출력값
    # print(f'tags :  {tags}, text: {text}')
    # print(f'trained_doc_vec : {trained_doc_vec}')
    # print(f'inferred_doc_vec : {inferred_doc_vec}')
    # print('--'* 20 )


new_txt_path = '/Users/heyon/Desktop/KB/test/test1.txt'
new_txt = [' '.join(txt_to_text(new_txt_path)) ]
print('new text')
print(new_txt)
print('--'* 20 )


inferred_v = model.infer_vector(new_txt)

print(f'vector of new_txt {new_txt} : {inferred_v}')

most_similar_docs = model.docvecs.most_similar([inferred_v], topn=3)

for index, similarity in most_similar_docs:
    print(f'{index}, similarity : {similarity}')
