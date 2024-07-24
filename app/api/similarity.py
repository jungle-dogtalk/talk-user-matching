import os
from fastapi import APIRouter
from app.schemas import SimilarityRequest
from app.utils import normalize_vector, cosine_similarity
import numpy as np
import gensim
from gensim.models import KeyedVectors

router = APIRouter()

# 한국어 Word2Vec 모델 로드
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, '..', 'ko.bin')
absolute_file_path = os.path.abspath(file_path)
print(f"Loading model from: {absolute_file_path}")

# Word2Vec 모델 로드
model = gensim.models.Word2Vec.load(absolute_file_path)

@router.post("/")
async def calculate_similarity(request: SimilarityRequest):
    interestsA = request.interestsA
    interestsB = request.interestsB

    AIinterestsA = request.AIinterestsA
    AIinterestsB = request.AIinterestsB

  

    def get_word_vector(word, model):
        if word in model.wv:
            return model.wv[word]
        else:
            return np.zeros(model.vector_size)

    # 관심사를 벡터로 변환하고 정규화
    vectorsA = [normalize_vector(get_word_vector(interest, model)) for interest in interestsA]
    vectorsB = [normalize_vector(get_word_vector(interest, model)) for interest in interestsB]

    AIvectorsA = [normalize_vector(get_word_vector(interest, model)) for interest in AIinterestsA]
    AIvectorsB = [normalize_vector(get_word_vector(interest, model)) for interest in AIinterestsB]

    # 관심사 벡터가 비어있을 때 유사도를 0.0
    if not vectorsA or not vectorsB:
        return {"similarity": 0.0}

    if not AIvectorsA or not AIvectorsB:
        return {"similarity": 0.0}

    # 관심사 벡터의 평균 계산
    vectorA = normalize_vector(np.mean(vectorsA, axis=0))
    vectorB = normalize_vector(np.mean(vectorsB, axis=0))

    AIvectorA = normalize_vector(np.mean(AIvectorsA, axis=0))
    AIvectorB = normalize_vector(np.mean(AIvectorsB, axis=0))

    # 코사인 유사도 계산
    interest_similarity = cosine_similarity(vectorA, vectorB)
    AI_interest_similarity = cosine_similarity(AIvectorA, AIvectorB)
    

     # 가중치를 적용한 전체 유사도 계산 (기본 관심사: 70%, AI 관심사: 30%)
    weight_interests = 0.7
    weight_AI_interests = 0.3
    total_similarity = (interest_similarity * weight_interests) + (AI_interest_similarity * weight_AI_interests)
    
    return {"similarity": float(total_similarity)}