from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    """
    TF-IDF based content recommendation engine.
    """

    def __init__(self, content_df):

        self.content_df = content_df.reset_index(drop=True)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            ngram_range=(1, 2)
        )

        self.matrix = self.vectorizer.fit_transform(
            self.content_df["content"]
        )

    def recommend(self, query, top_k=5):

        if not query or not str(query).strip():
            return []

        query_vector = self.vectorizer.transform(
            [str(query)]
        )

        similarity_scores = cosine_similarity(
            query_vector,
            self.matrix
        ).flatten()

        ranked_indices = similarity_scores.argsort()[::-1]

        recommendations = []

        for index in ranked_indices[:top_k]:

            recommendations.append(
                {
                    "id": int(
                        self.content_df.iloc[index]["id"]
                    ),
                    "question": self.content_df.iloc[index][
                        "question"
                    ],
                    "answer": self.content_df.iloc[index][
                        "answer"
                    ],
                    "score": round(
                        float(similarity_scores[index]),
                        4
                    ),
                }
            )

        return recommendations