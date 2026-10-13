# Week 3 Baseline Model Report

## 1. Objective

Build a baseline recommendation system using student performance and content engagement data to recommend subjects for further learning.

## 2. Dataset Summary

- Student performance records: 1,000
- Unique subjects: 10
- Content engagement records: 600
- Test cases available: 50

## 3. Data Pipeline

The data pipeline loads the student performance, content engagement, and EdTech test datasets. It standardizes column names, removes duplicate records, and saves the cleaned datasets in `data/processed/`.

## 4. Baseline Model

The baseline model calculates recommendation scores using average post-test scores and course completion percentages. Student-level performance and engagement information are used to adjust recommendations for existing students.

The model supports:

- **Warm-start:** Recommendations for a student present in the dataset.
- **Cold-start:** Recommendations for an unknown student.

## 5. Evaluation Results

All five functional checks passed:

- Warm-start returns five recommendations.
- Cold-start returns five recommendations.
- Warm-start recommendations contain no duplicate subjects.
- Cold-start recommendations contain no duplicate subjects.
- Recommendation scores are finite.

Detailed results are saved in `reports/evaluation_results.json`.

## 6. Evaluation Limitation

Precision@5 has not yet been measured because the provided test cases evaluate student risk labels rather than relevant course recommendations. A suitable recommendation relevance dataset is required to calculate this metric accurately.

## 7. Conclusion

The data ingestion and preprocessing pipeline and baseline recommendation model are implemented. Initial functional evaluation passed all five checks. Further work is required to measure recommendation accuracy and implement the remaining project requirements.
