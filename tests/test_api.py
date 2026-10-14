
from fastapi.testclient import TestClient
from src.api import app, performance

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_cold_start_recommendations():
    response = client.post(
        "/recommend",
        json={"student_id": "NEW-STUDENT", "top_k": 5},
    )
    assert response.status_code == 200
    assert response.json()["mode"] == "Cold-start"
    assert len(response.json()["recommendations"]) == 5


def test_warm_start_recommendations():
    student_id = str(performance["student_id"].iloc[0])
    response = client.post(
        "/recommend",
        json={"student_id": student_id, "top_k": 5},
    )
    assert response.status_code == 200
    assert response.json()["mode"] == "Warm-start"


def test_invalid_request():
    response = client.post(
        "/recommend",
        json={"student_id": "NEW-STUDENT", "top_k": 0},
    )
    assert response.status_code == 422
