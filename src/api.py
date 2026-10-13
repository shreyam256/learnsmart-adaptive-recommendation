from fastapi import FastAPI
from pydantic import BaseModel

from src.data_pipeline import (
    load_labelled_samples,
    prepare_content_items,
)

from src.recommender import ContentBasedRecommender


app = FastAPI(
    title="Cynaris Adaptive Learning Recommendation Engine",
    description="Baseline content-based recommendation API",
    version="0.1.0",
)


labelled_samples = load_labelled_samples()

content_df = prepare_content_items(
    labelled_samples
)

recommender = ContentBasedRecommender(
    content_df
)


class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "TF-IDF Content-Based Baseline"
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):

    recommendations = recommender.recommend(
        request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "recommendations": recommendations
    }