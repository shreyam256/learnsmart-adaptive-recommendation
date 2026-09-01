# Adaptive Learning Recommendation Engine

## Research and Architecture Design

### 1. Project Objective

The objective of this project is to build an adaptive learning recommendation engine that recommends the next suitable course for a learner.

The system will use a hybrid recommendation approach combining:

- Collaborative Filtering
- Content-Based Filtering
- Learner quiz scores
- Previously completed courses
- Course similarity
- Learner behaviour

The system will support both cold-start and warm-start users.

The final system will expose recommendations through a REST API using FastAPI.

---

## 2. Research Review

### Research 1 — Matrix Factorization Techniques for Recommender Systems

Matrix factorization is a widely used collaborative filtering technique.

It represents users and items using lower-dimensional vectors called latent factors. The interaction between a user and an item can then be used to predict how relevant that item may be to the user.

### Relevance to This Project

Matrix factorization can be used to learn relationships between learners and courses based on course completion, quiz scores, and other interactions.

### Planned Use

Collaborative filtering will be used as one component of the hybrid recommendation engine for warm-start users.

---

### Research 2 — Item-Based Collaborative Filtering Recommendation Algorithms

Item-based collaborative filtering recommends items by identifying items that are similar based on user interaction patterns.

### Relevance to This Project

If a learner has completed a particular course, the system can identify other courses that learners with similar course histories have also completed or preferred.

### Planned Use

Item/course similarity can help generate candidate courses for learners who already have sufficient interaction history.

---

### Research 3 — Content-Based Recommendation Systems

Content-based recommendation recommends items based on their characteristics and their similarity to items previously preferred by a user.

### Relevance to This Project

Courses can be represented using features such as:

- Course category
- Course topic
- Difficulty level
- Skills covered
- Course description

The learner's completed courses can then be compared with available courses to identify relevant next courses.

### Planned Use

Content-based filtering will provide recommendations based on course characteristics and the learner's learning history.

---

## 3. Proposed Recommendation Architecture

The proposed system will use a hybrid recommendation architecture.

### Input

The system receives:

- Learner ID
- Completed courses
- Quiz scores
- Available courses
- Course metadata

### Processing Pipeline

1. Load and validate learner and course data.
2. Preprocess course metadata.
3. Calculate content-based course similarity.
4. Build learner-course interaction data.
5. Generate collaborative filtering recommendations.
6. Combine collaborative and content-based scores.
7. Handle cold-start learners.
8. Rank candidate courses.
9. Return the top 5 recommended courses.

### Architecture

Learner Data
→ Data Preprocessing
→ Feature Engineering
→ Content-Based Filtering

- Collaborative Filtering
  → Hybrid Recommendation Engine
  → Ranking
  → Top-5 Recommendations
  → FastAPI REST API

  ***

## 4. Cold-Start Strategy

A cold-start learner is a learner with little or no previous interaction history.

For a new learner, collaborative filtering cannot reliably make recommendations because there is not enough historical interaction data.

Therefore, the system will initially use:

- Course popularity
- Course difficulty
- Course category
- Course prerequisites
- Initial quiz performance
- Course content similarity

As the learner completes courses and generates more interaction data, the system can gradually transition to the warm-start recommendation strategy.

---

## 5. Warm-Start Strategy

A warm-start learner has sufficient historical interaction data.

For these learners, the system will use:

- Previously completed courses
- Quiz scores
- Similar learners
- Course similarity
- Collaborative filtering scores
- Content-based scores

The final recommendation score will combine the outputs of collaborative and content-based filtering.

---

## 6. Hybrid Recommendation Strategy

The system will combine both recommendation approaches.

A weighted score can be calculated as:

Hybrid Score = α × Collaborative Score + (1 − α) × Content Score

where α controls the contribution of collaborative filtering.

The value of α can be tuned using validation data.

Quiz performance may also be incorporated into the ranking stage so that courses appropriate to the learner's current ability level are prioritised.

---

## 7. Evaluation Metrics

### Precision@5

The primary acceptance metric will be Precision@5.

Precision@5 measures how many of the five recommended courses are relevant to the learner.

Target:

**Precision@5 >= 0.60**

The system will evaluate the top five recommendations against labelled or held-out relevant courses.

### Additional Metrics

The following metrics may also be monitored:

- Recall@5
- F1 Score
- Coverage
- Cold-start recommendation success
- Warm-start recommendation success

---

## 8. A/B Testing

The project brief requires an A/B test using 100 sample users.

The users will be divided into two groups:

### Group A — Baseline

Users receive recommendations from a baseline recommendation strategy.

### Group B — Adaptive Hybrid Model

Users receive recommendations from the proposed hybrid recommendation engine.

The two groups will be compared using suitable recommendation or engagement metrics.

Possible measurements include:

- Course click-through rate
- Course completion rate
- Recommendation acceptance rate
- Average quiz performance

The results will be documented and added to the GitHub repository.

---

## 9. REST API

The recommendation engine will be exposed through FastAPI.

A planned endpoint is:

### GET /recommend/{user_id}

The endpoint will return the top recommended courses for a learner.

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
