import logging
import numpy as np
from sqlalchemy.orm import Session
from app.models.database import Evidence, Law
from app.services.faiss_connector import load_faiss_index, evidence_ids, EVIDENCE_INDEX_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def decide_neighbors(rerank_score, min_neighbors=1, max_neighbors=5):
    """Dynamic control of number of neighbors based on rerank_score."""
    if rerank_score >= 0.9:
        return max_neighbors
    elif rerank_score >= 0.8:
        return max_neighbors - 1
    elif rerank_score >= 0.7:
        return max_neighbors - 2
    elif rerank_score >= 0.6:
        return max_neighbors - 3
    else:
        return min_neighbors

def expand_neighbors(session: Session, documents, max_neighbors_law=5, max_neighbors_evidence=5):
    """
    Expand 1-hop neighbors for documents based on their type and rerank score using Session.
    """
    graph = {
        "nodes": [],
        "edges": []
    }

    added_node_ids = set()
    evidence_index, evidence_id_list = load_faiss_index(session, EVIDENCE_INDEX_ID, 1536)
    evidence_ids.clear()
    evidence_ids.extend(evidence_id_list)

    for doc in documents:
        doc_id = doc['id']
        doc_type = doc['type']
        rerank_score = doc.get('rerank_score', 0.5)

        if doc_id not in added_node_ids:
            graph["nodes"].append({
                "id": doc_id,
                "type": doc_type,
                "description": doc['description'],
                "metadata": doc.get('metadata', {}),  # ✅ 防止 KeyError
                "rerank_score": rerank_score
            })
            added_node_ids.add(doc_id)

        if doc_type == "law":
            # Dynamic neighbors for law
            num_neighbors = decide_neighbors(rerank_score, min_neighbors=1, max_neighbors=max_neighbors_law)

            related_ids = []
            metadata = doc.get('metadata', {})
            if metadata:
                try:
                    related_ids = metadata.get('related_ids', [])
                except Exception as e:
                    logger.warning(f"Failed to parse metadata for law {doc_id}: {e}")

            related_ids = related_ids[:num_neighbors]

            for neighbor_id in related_ids:
                neighbor_row = session.query(Law).filter(Law.id == neighbor_id).first()
                if not neighbor_row:
                    continue

                if neighbor_id not in added_node_ids:
                    graph["nodes"].append({
                        "id": neighbor_row.id,
                        "type": neighbor_row.type,
                        "description": neighbor_row.description,
                        "metadata": neighbor_row.metadata or {}
                    })
                    added_node_ids.add(neighbor_id)

                graph["edges"].append({
                    "source": doc_id,
                    "target": neighbor_id,
                    "relation": "law_related"
                })

        elif doc_type == "evidence":
            # Dynamic neighbors for evidence
            num_neighbors = decide_neighbors(rerank_score, min_neighbors=1, max_neighbors=max_neighbors_evidence)

            try:
                idx = evidence_ids.index(doc_id)
            except ValueError:
                logger.warning(f"Evidence id {doc_id} not found in evidence_ids.")
                continue

            query_vector = np.zeros((1, 1536), dtype='float32')
            query_vector[0] = evidence_index.reconstruct(idx)

            distances, neighbors = evidence_index.search(query_vector, num_neighbors + 1)
            neighbor_ids = [evidence_ids[j] for j in neighbors[0] if j != idx][:num_neighbors]

            for neighbor_id in neighbor_ids:
                neighbor_row = session.query(Evidence).filter(Evidence.id == neighbor_id).first()
                if not neighbor_row:
                    continue

                if neighbor_id not in added_node_ids:
                    graph["nodes"].append({
                        "id": neighbor_row.id,
                        "type": neighbor_row.type,
                        "description": neighbor_row.description,
                        "metadata": neighbor_row.metadata or {}
                    })
                    added_node_ids.add(neighbor_id)

                graph["edges"].append({
                    "source": doc_id,
                    "target": neighbor_id,
                    "relation": "evidence_similar"
                })

    logger.info(f"Dynamic graph expansion completed. {len(graph['nodes'])} nodes, {len(graph['edges'])} edges generated.")

    return graph


