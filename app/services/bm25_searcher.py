from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from sqlalchemy.orm import Session
from app.models.database import Evidence, Law
import nltk

# --- Ensure NLTK Resources ---
def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

ensure_nltk_resources()

# --- Load documents using SQLAlchemy Session ---
def load_documents_via_session(session: Session):
    documents = []

    evidence_rows = session.query(Evidence.id, Evidence.description).all()
    for row in evidence_rows:
        if row.description:
            documents.append({
                'id': row.id,
                'type': 'evidence',
                'description': row.description
            })

    law_rows = session.query(Law.id, Law.description).all()
    for row in law_rows:
        if row.description:
            documents.append({
                'id': row.id,
                'type': 'law',
                'description': row.description
            })

    return documents

# --- BM25 Retriever ---
class BM25Retriever:
    def __init__(self, documents):
        self.documents = documents
        self.doc_texts = [doc['description'] for doc in documents]

        self.tokenized_corpus = [word_tokenize(text.lower(), preserve_line=True) for text in self.doc_texts]

        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query, top_k=5):
        tokenized_query = word_tokenize(query.lower(), preserve_line=True)
        scores = self.bm25.get_scores(tokenized_query)
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_k_indices:
            doc = self.documents[idx]
            results.append({
                "id": doc['id'],
                "type": doc['type'],
                "description": doc['description'],
                "score": float(scores[idx])
            })
        return results
