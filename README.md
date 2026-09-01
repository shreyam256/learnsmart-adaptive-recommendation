# Adaptive Learning Recommendation Engine

## 1. Project Overview

The Adaptive Learning Recommendation Engine is a machine learning-based system designed to recommend suitable next courses for learners based on their previous learning activity and performance.

The proposed system combines collaborative filtering and content-based filtering to generate personalised course recommendations.

The system is designed to support both new learners with limited history and existing learners with sufficient learning history.

---

## 2. Objectives

The main objectives are:

- Recommend suitable next courses for learners.
- Use completed courses and quiz scores as learner signals.
- Combine collaborative and content-based filtering.
- Support cold-start and warm-start learners.
- Achieve a target Precision@5 of at least 0.60.
- Provide recommendations through a REST API using FastAPI.
- Evaluate the recommendation strategy using an A/B test with 100 sample users.

---

## 3. Technologies

- Python 3.11
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Uvicorn
- Jupyter Notebook
- Git
- GitHub

---

## 4. Proposed Architecture

```text
Learner Data
     |
     v
Data Preprocessing
     |
     v
Feature Engineering
     |
     +-------------------------+
     |                         |
     v                         v
Content-Based             Collaborative
Filtering                 Filtering
     |                         |
     +-----------+-------------+
                 |
                 v
        Hybrid Recommendation
                 |
                 v
          Ranking Engine
                 |
                 v
       Top 5 Recommendations
                 |
                 v
           FastAPI REST API
```

---

## 5. Recommendation Strategy

### Content-Based Filtering

Content-based filtering will recommend courses based on course characteristics such as:

- Course category
- Topic
- Difficulty
- Skills
- Course description

The system will compare courses previously completed by the learner with available courses.

### Collaborative Filtering

Collaborative filtering will identify relationships between learners and courses using historical learner-course interactions.

It will be primarily used for learners with sufficient interaction history.

### Hybrid Recommendation

The final recommendation will combine collaborative and content-based scores.

A weighted hybrid score will be considered:

```text
Hybrid Score = α × Collaborative Score
             + (1 − α) × Content Score
```

---

## 6. Cold-Start Handling

For learners with little or no previous interaction history, collaborative filtering may not have enough information.

The cold-start strategy will therefore use available course information, popularity, prerequisites, and initial learner performance signals to generate recommendations.

---

## 7. Warm-Start Handling

For learners with sufficient learning history, recommendations will use:

- Completed courses
- Quiz scores
- Course similarity
- Similar learner behaviour
- Collaborative filtering
- Content-based filtering

---

## 8. Evaluation

The primary evaluation metric is:

**Precision@5 >= 0.60**

Additional metrics that may be evaluated include:

- Recall@5
- F1 Score
- Recommendation coverage
- Cold-start performance
- Warm-start performance

---

## 9. A/B Testing

The project will include an A/B test using 100 sample users.

### Group A

Users will receive recommendations from a baseline recommendation strategy.

### Group B

Users will receive recommendations from the proposed adaptive hybrid recommendation engine.

The results will be compared using suitable recommendation and engagement metrics.

---

## 10. REST API

The recommendation engine will be exposed through FastAPI.

Planned endpoint:

```text
GET /recommend/{user_id}
```

Example response:

```json
{
  "user_id": "U001",
  "recommendations": [
    {
      "course_id": "C101",
      "score": 0.91
    },
    {
      "course_id": "C205",
      "score": 0.86
    }
  ]
}
```

---

## 11. Project Structure

```text
Cynaris_Adaptive_Learning/
|
├── data/
│   ├── aiml_training_data.csv
│   ├── aiml_labelled_samples.json
│   └── aiml_test_cases.txt
|
├── notebooks/
│   └── 01_data_exploration.ipynb
|
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── data_pipeline.py
|
├── tests/
|
├── README.md
├── RESEARCH.md
└── requirements.txt
```

The `src` directory will contain the project source code, while `tests` will contain testing code. This separation is a common Python project structure.

---

## 12. Current Data-Pack Status

The currently provided data pack contains:

- `aiml_training_data.csv` — text, intent and confidence fields
- `aiml_labelled_samples.json` — question, context, answer and relevance labels
- `aiml_test_cases.txt` — mixed AI/ML test cases

These files do not directly contain the learner-course interaction fields required for the proposed adaptive course recommendation engine.

Therefore, the provided data will be preserved without modification while clarification is requested regarding the appropriate learner/course dataset.

---

## 13. Current Progress

### Week 1 — Checkpoint 1

- [x] Project environment setup
- [x] Dataset inspection
- [x] Research documentation
- [x] Initial architecture design
- [x] Evaluation metrics defined
- [ ] README finalisation
- [ ] Data pipeline skeleton
- [ ] Git commits and pull request
- [ ] Mentor clarification regarding recommendation dataset

---

## 14. Future Work

The planned implementation stages are:

1. Obtain or confirm the correct learner/course dataset.
2. Build the data preprocessing pipeline.
3. Perform feature engineering.
4. Implement content-based filtering.
5. Implement collaborative filtering.
6. Develop the hybrid recommendation engine.
7. Implement cold-start and warm-start strategies.
8. Evaluate Precision@5.
9. Build the FastAPI REST API.
10. Perform A/B testing on 100 sample users.
11. Document results and final implementation.

## Evaluation Metrics

The recommendation engine will be evaluated using ranking-based recommendation metrics.

### Precision@5

Precision@5 measures how many of the top 5 recommended courses are relevant to the learner.

**Formula:**

Precision@5 = Relevant courses in Top 5 / 5

The project acceptance target is:

**Precision@5 ≥ 0.60**

### Recall@5

Recall@5 measures how many of the relevant courses available to the learner are successfully included in the top 5 recommendations.

### Hit Rate@5

Hit Rate@5 measures whether at least one relevant course appears among the top 5 recommendations.

### A/B Testing

The recommendation system will also be evaluated through an A/B test using 100 sample users. The test will compare the proposed recommendation approach against a baseline to measure recommendation effectiveness and user engagement.
