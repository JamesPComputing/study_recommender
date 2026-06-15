from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import get_db

def get_recommendations(user_input, difficulty_filter='All', top_n=5):
    """
    Returns top N study resource recommendations for a given topic.
    Uses TF-IDF vectorisation and cosine similarity.
    """
    conn = get_db()
    cursor = conn.cursor()

    if difficulty_filter and difficulty_filter != 'All':
        cursor.execute(
            'SELECT * FROM resources WHERE difficulty = ?', (difficulty_filter,)
        )
    else:
        cursor.execute('SELECT * FROM resources')

    resources = cursor.fetchall()
    conn.close()

    if not resources:
        return []

    # Combine description and topic_tags for richer matching
    corpus = [f"{r['description']} {r['topic_tags']}" for r in resources]

    # Append user query to corpus for vectorisation
    corpus_with_query = corpus + [user_input]

    # TF-IDF vectorisation
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(corpus_with_query)

    # Cosine similarity: user query vector vs all resource vectors
    query_vector = tfidf_matrix[-1]
    resource_vectors = tfidf_matrix[:-1]
    similarities = cosine_similarity(query_vector, resource_vectors).flatten()

    # Sort by similarity descending, take top N
    top_indices = similarities.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        if similarities[idx] > 0:
            resource = dict(resources[idx])
            resource['score'] = round(float(similarities[idx]), 2)
            results.append(resource)

    return results