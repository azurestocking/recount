# import faiss
# import numpy as np
# import openai
# import logging
# import tempfile
# from sqlalchemy.orm import Session
# from app.config.config import OPENAI_API_KEY
# from app.models.database import Evidence, Law, FaissIndex
#
# # Logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # FAISS Index IDs
# EVIDENCE_INDEX_ID = "evidence-index-id-1234"
# LAW_INDEX_ID = "law-index-id-5678"
#
# # Local caches
# evidence_ids = []
# law_ids = []
#
# # Embedding config
# EMBEDDING_DIM = 1536
# EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
#
# # --- Embedding ---
# def get_embedding(text: str, api_key=OPENAI_API_KEY, model=EMBEDDING_MODEL_NAME):
#     """Generate OpenAI embedding"""
#     client = openai.OpenAI(api_key=api_key)
#     response = client.embeddings.create(input=[text], model=model)
#     if not response or not response.data:
#         logger.error(f"OpenAI API returned empty embedding: {response}")
#         return None
#     return np.array(response.data[0].embedding, dtype=np.float32)
#
# # --- FAISS Save/Load ---
#
# # def save_faiss_index(session: Session, index: faiss.Index, index_id: str):
# #     """Save FAISS index to database"""
# #     try:
# #         binary = faiss.serialize_index(index)
# #         record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
# #         if record:
# #             record.index_data = binary
# #         else:
# #             record = FaissIndex(id=index_id, index_data=binary)
# #             session.add(record)
# #         session.commit()
# #     except Exception as e:
# #         session.rollback()
# #         logger.error(f"Failed to save FAISS index: {e}")
# #         raise
#
# def save_faiss_index(session: Session, index: faiss.Index, index_id: str, id_list: list):
#     """
#     Save FAISS index and id_list into database.
#     """
#     try:
#         import tempfile
#         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#             faiss.write_index(index, tmp_file.name)
#             tmp_file.flush()
#             tmp_file.seek(0)
#             index_binary = tmp_file.read()
#
#         record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
#         if record:
#             record.index_data = index_binary
#             record.id_list = id_list
#         else:
#             record = FaissIndex(id=index_id, index_data=index_binary, id_list=id_list)
#             session.add(record)
#         session.commit()
#         logger.info(f"✅ Saved FAISS index and id_list for {index_id}")
#     except Exception as e:
#         session.rollback()
#         logger.error(f"Failed to save FAISS index: {e}")
#         raise
#
# # def load_faiss_index(session: Session, index_id: str, dim: int) -> faiss.Index:
# #     """Load FAISS index from database"""
# #     try:
# #         record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
# #         if record and record.index_data:
# #             with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
# #                 tmp_file.write(record.index_data)
# #                 tmp_file.flush()
# #                 index = faiss.read_index(tmp_file.name)
# #             return index
# #         else:
# #             logger.info(f"No FAISS index found for {index_id}, creating new one.")
# #             return faiss.IndexFlatIP(dim)
# #     except Exception as e:
# #         logger.warning(f"Failed to deserialize FAISS index: {e}")
# #         return faiss.IndexFlatIP(dim)
#
# def load_faiss_index(session: Session, index_id: str, dim: int):
#     """
#     Load FAISS index and id_list from database, using tempfile for deserialization.
#     """
#     try:
#         record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
#         if record and record.index_data:
#             with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#                 tmp_file.write(record.index_data)
#                 tmp_file.flush()
#                 index = faiss.read_index(tmp_file.name)
#             id_list = record.id_list if record.id_list else []
#             logger.info(f"✅ Loaded FAISS index and {len(id_list)} ids for {index_id}")
#             return index, id_list
#         else:
#             logger.info(f"No FAISS index found for {index_id}, creating new one.")
#             return faiss.IndexFlatIP(dim), []
#     except Exception as e:
#         logger.warning(f"Failed to deserialize FAISS index: {e}")
#         return faiss.IndexFlatIP(dim), []
#
#
# # --- Evidence operations ---
# def save_evidence_embedding(session: Session, evidence_id: str, text: str):
#     """Save evidence embedding into FAISS"""
#     emb = get_embedding(text)
#     if emb is None:
#         logger.error(f"Failed to generate embedding for evidence {evidence_id}")
#         return
#     emb = np.expand_dims(emb, axis=0)  # (1, dim)
#     index = load_faiss_index(session, EVIDENCE_INDEX_ID, EMBEDDING_DIM)
#     index.add(emb)
#     save_faiss_index(session, index, EVIDENCE_INDEX_ID)
#     evidence_ids.append(evidence_id)
#     # load_evidence_ids(session)
#
# def load_evidence_ids(session: Session):
#     """Load all evidence IDs ordered by FAISS index insertion order."""
#     global evidence_ids
#
#     # 全部查出来，保证evidence_ids长度和FAISS index一一对应！
#     evidence_ids = [row.id for row in session.query(Evidence.id).order_by(Evidence.created_at.asc()).all()]
#
#     logger.info(f"✅ Refreshed evidence_id cache, total {len(evidence_ids)} evidence IDs loaded.")
#
#
# def save_evidence_and_refresh(session: Session, evidence_id: str, text: str):
#     save_evidence_embedding(session, evidence_id, text)
#     load_evidence_ids(session)
#
#
# def search_evidence(session: Session, query: str, top_k: int = 5):
#     """Search evidence by query"""
#     emb = get_embedding(query)
#     if emb is None:
#         return []
#     emb = np.expand_dims(emb, axis=0)
#     index = load_faiss_index(session, EVIDENCE_INDEX_ID, EMBEDDING_DIM)
#     distances, indices = index.search(emb, top_k)
#
#     results = []
#     for idx, score in zip(indices[0], distances[0]):
#         if idx != -1 and idx < len(evidence_ids):
#             evid = evidence_ids[idx]
#             row = session.query(Evidence).filter(Evidence.id == evid).first()
#             if row:
#                 results.append({
#                     "id": evid,
#                     "score": float(score),
#                     "description": row.description,
#                     "file_path": row.file_path,
#                     "metadata": row.metadata
#                 })
#     return results
#
# # --- Law operations ---
# def save_law_embedding(session: Session, law_id: str, text: str):
#     """Save law embedding into FAISS"""
#     emb = get_embedding(text)
#     if emb is None:
#         logger.error(f"Failed to generate embedding for law {law_id}")
#         return
#     emb = np.expand_dims(emb, axis=0)
#     index = load_faiss_index(session, LAW_INDEX_ID, EMBEDDING_DIM)
#     index.add(emb)
#     save_faiss_index(session, index, LAW_INDEX_ID)
#     law_ids.append(law_id)
#
# def load_law_ids(session: Session):
#     """Load law IDs from database"""
#     global law_ids
#     law_ids = [l.id for l in session.query(Law.id).order_by(Law.created_at.asc()).all()]
#
# def search_law(session: Session, query: str, top_k: int = 5):
#     """Search law by query"""
#     emb = get_embedding(query)
#     if emb is None:
#         return []
#     emb = np.expand_dims(emb, axis=0)
#     index = load_faiss_index(session, LAW_INDEX_ID, EMBEDDING_DIM)
#     distances, indices = index.search(emb, top_k)
#
#     results = []
#     for idx, score in zip(indices[0], distances[0]):
#         if idx != -1 and idx < len(law_ids):
#             lawid = law_ids[idx]
#             row = session.query(Law).filter(Law.id == lawid).first()
#             if row:
#                 results.append({
#                     "id": lawid,
#                     "score": float(score),
#                     "description": row.description,
#                     "file_path": row.file_path,
#                     "metadata": row.metadata
#                 })
#     return results

import faiss
import numpy as np
import openai
import logging
import json
import tempfile
from sqlalchemy.orm import Session
from app.config.config import OPENAI_API_KEY as EMBEDDING_MODEL_API_KEY
from app.models.database import Evidence, Law, FaissIndex
from typing import Tuple, List

EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FAISS Index IDs
EVIDENCE_INDEX_ID = "evidence-index-id-1234"
LAW_INDEX_ID = "law-index-id-5678"

# Local caches
evidence_ids = []
law_ids = []

# Embedding Dimension
EMBEDDING_DIM = 1536

# --- Embedding ---
def get_embedding(text: str, api_key=EMBEDDING_MODEL_API_KEY, model=EMBEDDING_MODEL_NAME):
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(input=[text], model=model)
    if not response or not response.data:
        logger.error(f"OpenAI API returned empty embedding: {response}")
        return None
    return np.array(response.data[0].embedding, dtype=np.float32)

# --- Save FAISS Index ---
def save_faiss_index(session: Session, index: faiss.Index, index_id: str, id_list: list):
    try:
        binary = faiss.serialize_index(index)
        record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
        if record:
            record.index_data = binary
            record.id_list = json.dumps(id_list)
        else:
            record = FaissIndex(id=index_id, index_data=binary, id_list=json.dumps(id_list))
            session.add(record)
        session.commit()
        logger.info(f"✅ Saved FAISS index and ID list for {index_id}.")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to save FAISS index: {e}")
        raise

# --- Load FAISS Index ---
# def load_faiss_index(session: Session, index_id: str, dim: int):
#     try:
#         record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
#         if record and record.index_data:
#             with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#                 tmp_file.write(record.index_data)
#                 tmp_file.flush()
#                 index = faiss.read_index(tmp_file.name)
#         else:
#             logger.info(f"No FAISS index found for {index_id}, creating new one.")
#             index = faiss.IndexFlatIP(dim)
#
#         id_list = []
#         if record and record.id_list:
#             id_list = json.loads(record.id_list)
#
#         return index, id_list
#     except Exception as e:
#         logger.warning(f"Failed to load FAISS index: {e}")
#         return faiss.IndexFlatIP(dim), []
def load_faiss_index(session: Session, index_id: str, dim: int) -> Tuple[faiss.Index, List[str]]:
    """Load FAISS index and ID list from database."""
    try:
        record = session.query(FaissIndex).filter(FaissIndex.id == index_id).first()
        if record and record.index_data:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(record.index_data)
                tmp_file.flush()
                index = faiss.read_index(tmp_file.name)
            id_list = json.loads(record.id_list) if record.id_list else []
            logger.info(f"✅ Loaded FAISS index with {len(id_list)} IDs.")
            return index, id_list
        else:
            logger.info(f"No FAISS index found for {index_id}, creating new one.")
            return faiss.IndexFlatIP(dim), []
    except Exception as e:
        logger.warning(f"Failed to deserialize FAISS index: {e}")
        return faiss.IndexFlatIP(dim), []



# --- Evidence operations ---
def save_evidence_embedding(session: Session, evidence_id: str, text: str):
    emb = get_embedding(text)
    if emb is None:
        logger.error(f"Failed to generate embedding for evidence {evidence_id}")
        return
    emb = np.expand_dims(emb, axis=0)
    index, ids = load_faiss_index(session, EVIDENCE_INDEX_ID, EMBEDDING_DIM)
    index.add(emb)
    ids.append(evidence_id)
    save_faiss_index(session, index, EVIDENCE_INDEX_ID, ids)
    logger.info(f"✅ Embedded evidence id: {evidence_id}")

# --- Law operations ---
def save_law_embedding(session: Session, law_id: str, text: str):
    emb = get_embedding(text)
    if emb is None:
        logger.error(f"Failed to generate embedding for law {law_id}")
        return
    emb = np.expand_dims(emb, axis=0)
    index, ids = load_faiss_index(session, LAW_INDEX_ID, EMBEDDING_DIM)
    index.add(emb)
    ids.append(law_id)
    save_faiss_index(session, index, LAW_INDEX_ID, ids)

# --- Load ID Caches ---
def load_evidence_ids(session: Session):
    global evidence_ids
    _, evidence_ids = load_faiss_index(session, EVIDENCE_INDEX_ID, EMBEDDING_DIM)
    logger.info(f"✅ Refreshed evidence_id cache, total {len(evidence_ids)} evidence IDs loaded.")

def load_law_ids(session: Session):
    global law_ids
    _, law_ids = load_faiss_index(session, LAW_INDEX_ID, EMBEDDING_DIM)
    logger.info(f"✅ Refreshed law_id cache, total {len(law_ids)} law IDs loaded.")

# --- Utility: Save and Refresh ---
def save_evidence_and_refresh(session: Session, evidence_id: str, text: str):
    save_evidence_embedding(session, evidence_id, text)
    load_evidence_ids(session)

def save_law_and_refresh(session: Session, law_id: str, text: str):
    save_law_embedding(session, law_id, text)
    load_law_ids(session)

# --- Utility: Search ---
def search_evidence(session: Session, query: str, top_k: int = 5):
    emb = np.expand_dims(get_embedding(query), axis=0)
    index, _ = load_faiss_index(session, EVIDENCE_INDEX_ID, EMBEDDING_DIM)
    distances, indices = index.search(emb, top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        if idx != -1 and idx < len(evidence_ids):
            evid = evidence_ids[idx]
            row = session.query(Evidence).filter(Evidence.id == evid).first()
            if row:
                results.append({
                    "id": evid,
                    "score": float(score),
                    "description": row.description,
                    "file_path": row.file_path,
                    "metadata": row.metadata
                })
    return results

def search_law(session: Session, query: str, top_k: int = 5):
    emb = np.expand_dims(get_embedding(query), axis=0)
    index, _ = load_faiss_index(session, LAW_INDEX_ID, EMBEDDING_DIM)
    distances, indices = index.search(emb, top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        if idx != -1 and idx < len(law_ids):
            lawid = law_ids[idx]
            row = session.query(Law).filter(Law.id == lawid).first()
            if row:
                results.append({
                    "id": lawid,
                    "score": float(score),
                    "description": row.description,
                    "file_path": row.file_path,
                    "metadata": row.metadata
                })
    return results

def save_evidence_and_refresh(session: Session, evidence_id: str, text: str):
    save_evidence_embedding(session, evidence_id, text)
    load_evidence_ids(session)
    logger.info(f"✅ After refresh, added evidence id: {evidence_id}")

