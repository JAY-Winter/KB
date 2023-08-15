import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def txt_to_text(file_path) -> list[str]:
    '''
    txt 파일을 text: [list] 로 분리
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        content = [file.read()]
    return content


# 모델 load
model = Doc2Vec.load('./test_model.model')

# 테스트 해볼 새로운 파일
new_txt_path = '/Users/heyon/Desktop/KB/test/test1.txt'
new_txt = [' '.join(txt_to_text(new_txt_path)) ]

print('new text')
print(new_txt)
print('--'* 20 )

# 새로운 파일에 대한 추론 벡터값
inferred_v = model.infer_vector(new_txt)

print(f'vector of new_txt {new_txt} : {inferred_v}')

# 새로운 파일을 벡터값과 추론한 벡터값을 비교해 가장 유사한 상위 3개 값
most_similar_docs = model.docvecs.most_similar([inferred_v], topn=3)

for index, similarity in most_similar_docs:
    print(f'{index}, similarity : {similarity}')
