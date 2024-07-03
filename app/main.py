from fastapi import FastAPI
from app.api.similarity import router as similarity_router

app = FastAPI()

app.include_router(similarity_router, prefix="/similarity")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)