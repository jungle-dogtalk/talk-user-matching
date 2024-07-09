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
    # listeningA = request.listeningA
    # listeningB = request.listeningB
    # speakingA = request.speakingA
    # speakingB = request.speakingB

    def get_word_vector(word, model):
        if word in model.wv:
            return model.wv[word]
        else:
            return np.zeros(model.vector_size)

    # 관심사를 벡터로 변환하고 정규화
    vectorsA = [normalize_vector(get_word_vector(interest, model)) for interest in interestsA]
    vectorsB = [normalize_vector(get_word_vector(interest, model)) for interest in interestsB]

    if not vectorsA or not vectorsB:
        return {"similarity": 0.0}

    # 관심사 벡터의 평균 계산
    vectorA = normalize_vector(np.mean(vectorsA, axis=0))
    vectorB = normalize_vector(np.mean(vectorsB, axis=0))

    # 코사인 유사도 계산
    interest_similarity = cosine_similarity(vectorA, vectorB)
    
    # 경청 지수, 발화 지수 보완 지수 계산
    # listening_speaking_complementary = (listeningA + speakingB) / 20
    # speaking_listening_complementary = (speakingA + listeningB) / 20

    # 관심사/경청/발화 지수 전체 계산
    # overall_similarity = (
    #     0.5 * interest_similarity +
    #     0.25 * listening_speaking_complementary +
    #     0.25 * speaking_listening_complementary
    # )

    return {"similarity": float(interest_similarity)}
