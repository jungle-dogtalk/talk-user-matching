from pydantic import BaseModel
from typing import List

# API의 데이터 모델을 정의
# Pydantic을 사용하여 요청(request) 및 응답(response) 데이터 구조와 유효성을 검사

class SimilarityRequest(BaseModel):
    interestsA: List[str]
    interestsB: List[str]
    # listeningA: int
    # listeningB: int
    # speakingA: int
    # speakingB: int
