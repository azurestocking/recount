import numpy as np
import faiss
from sqlalchemy.orm import Session
from app.models.database import Law
from app.services.faiss_connector import load_faiss_index, law_ids, LAW_INDEX_ID

# Load FAISS law index
# 注意！需要在调用外部传入session，再调用这里的load
# 比如外部：session = SessionLocal()
# law_index = load_faiss_index(session, LAW_INDEX_ID, 1536)
# 这样才统一

def generate_law_related_ids(session: Session, index, ids, max_neighbors=3):
    """
    For each law document, find top-k nearest neighbors and update metadata.related_ids using Session.
    """
    for i, doc_id in enumerate(ids):
        query_vector = np.zeros((1, 1536), dtype='float32')
        query_vector[0] = index.reconstruct(i)

        distances, neighbors = index.search(query_vector, max_neighbors + 1)  # +1 because first is itself
        related_ids = [ids[j] for j in neighbors[0] if j != i][:max_neighbors]

        # Fetch existing Law object
        law_record = session.query(Law).filter(Law.id == doc_id).first()
        if not law_record:
            continue

        # Update metadata
        metadata = {}
        if law_record.metadata:
            try:
                metadata = law_record.metadata if isinstance(law_record.metadata, dict) else eval(law_record.metadata)
            except Exception:
                metadata = {}

        metadata['related_ids'] = related_ids
        law_record.metadata = metadata

    session.commit()

