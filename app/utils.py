import numpy as np
import torch

#코사인 유사도 계산 
def cosine_similarity(vectorA, vectorB):
    dot_product = np.dot(vectorA, vectorB) # 두 벡터의 내적 계산
    normA = np.linalg.norm(vectorA)  
    normB = np.linalg.norm(vectorB)

    if normA == 0 or normB == 0:
        return 0.0 #벡터 중 하나의 크기가 0 이면 return 유사도 0.0 
    return dot_product / (normA * normB) 

#문장을 임베딩 벡터로 변환 
def get_sentence_embedding(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

#벡터 정규화 
def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    #벡터의 크기가 0이면 원래 벡터 return 
    if norm == 0:
        return vector
    return vector / norm
