from fastapi import APIRouter
from app.schemas import SimilarityRequest
from app.utils import get_sentence_embedding, normalize_vector, cosine_similarity
from transformers import AutoModel, AutoTokenizer
import numpy as np

router = APIRouter()

# KLUE/BERT 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained('klue/bert-base')
model = AutoModel.from_pretrained('klue/bert-base')

@router.post("/")
async def calculate_similarity(request: SimilarityRequest):
    interestsA = request.interestsA
    interestsB = request.interestsB
    listeningA = request.listeningA
    listeningB = request.listeningB
    speakingA = request.speakingA
    speakingB = request.speakingB

    # 관심사를 벡터로 변환하고 정규화
    vectorsA = [normalize_vector(get_sentence_embedding(interest, tokenizer, model)) for interest in interestsA]
    vectorsB = [normalize_vector(get_sentence_embedding(interest, tokenizer, model)) for interest in interestsB]

    if not vectorsA or not vectorsB:
        return {"similarity": 0.0}

    # 관심사 벡터의 평균 계산
    vectorA = normalize_vector(np.mean(vectorsA, axis=0))
    vectorB = normalize_vector(np.mean(vectorsB, axis=0))

    # 코사인 유사도 계산
    interest_similarity = cosine_similarity(vectorA, vectorB)
    
    # 경청 지수, 발화 지수 보완 지수 계산
    listening_speaking_complementary = (listeningA + speakingB) / 20
    speaking_listening_complementary = (speakingA + listeningB) / 20

    # 관심사/경청/발화 지수 전체 계산
    #   overall_similarity = (
        # 0.5 * interest_similarity +
        # 0.25 * listening_speaking_complementary +
        # 0.25 * speaking_listening_complementary
    # )
    
    overall_similarity = interest_similarity

    return {"similarity": float(overall_similarity)}
