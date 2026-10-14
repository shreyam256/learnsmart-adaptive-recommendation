# Cynaris Adaptive Learning - API Integration and Load Test Report

## 1. Overview

The recommendation model was integrated with a FastAPI serving layer to provide personalized course recommendations.

## 2. API Endpoints

- GET /health - Checks API health.
- POST /recommend - Returns course recommendations for a student.
- Interactive API documentation: /docs

## 3. Integration Testing

Automated tests were executed using pytest.

- Total tests: 4
- Passed: 4
- Failed: 0

Tests covered API health, cold-start recommendations, warm-start recommendations, and invalid input validation.

## 4. Load Testing

The API was tested locally using 50 concurrent requests.

| Metric              |       Observed Result |
| ------------------- | --------------------: |
| Total requests      |                    50 |
| Concurrent requests |                    50 |
| Successful requests |                    50 |
| Failed requests     |                     0 |
| Total test time     |         1.513 seconds |
| Average latency     |            1204.13 ms |
| Median latency      |            1203.62 ms |
| P95 latency         |            1259.45 ms |
| Throughput          | 33.06 requests/second |

## 5. Conclusion

All 50 requests completed successfully with no failures during this local test. The measured average latency was approximately 1.20 seconds per request. Further performance optimization and testing in a deployed environment may be required.

## 6. Project Files

- src/api.py
- src/baseline_model.py
- tests/test_api.py
- tests/load_test.py
- reports/serving_layer_report.md
