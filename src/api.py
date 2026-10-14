
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.baseline_model import (
    load_data,
    build_baseline,
    recommend_courses,
)

app = FastAPI(
    title="Cynaris Adaptive Learning API",
    description="Personalized course recommendations for students",
    version="1.0.0",
)

# Load the processed datasets and prepare the recommendation model
performance, engagement = load_data()

subject_stats, engagement_stats = build_baseline(
    performance, engagement
)


class RecommendationRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=100)
    top_k: int = Field(default=5, ge=1, le=10)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model": "EdTech Baseline Recommendation Model",
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):
    try:
        mode, results = recommend_courses(
            request.student_id.strip(),
            performance,
            subject_stats,
            engagement_stats,
            top_n=request.top_k,
        )

        recommendations = [
            {
                "subject": str(row["subject"]),
                "recommendation_score": round(
                    float(row["recommendation_score"]), 4
                ),
            }
            for _, row in results.iterrows()
        ]

        return {
            "student_id": request.student_id.strip(),
            "mode": mode,
            "recommendations": recommendations,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Recommendation could not be generated.",
        ) from error
