from app.models.database import Evidence, TimelineEvent
from app.services.faiss_connector import save_evidence_embedding
import logging

logger = logging.getLogger(__name__)

def save_extracted_info(db_session, conversation_id, outputs):
    """Save newly extracted evidences and events into database and FAISS index."""
    try:
        # Save evidences
        evidences = outputs.get("deduplicated_evidence", [])
        for evidence_item in evidences:
            evidence = Evidence(
                conversation_id=conversation_id,
                type=evidence_item["type"],
                file_path=evidence_item.get("file_path", ""),
                description=evidence_item["description"],
                metadata=evidence_item.get("metadata", None)
            )
            db_session.add(evidence)
            db_session.flush()  # Get id

            # Save to FAISS
            if evidence.description:
                save_evidence_embedding(db_session, evidence.id, evidence.description)

        # Save events
        events = outputs.get("deduplicated_events", [])
        for event_item in events:
            event = TimelineEvent(
                conversation_id=conversation_id,
                event_date=event_item.get("event_date", None),  # Optional
                description=event_item["description"],
                confidence_score=event_item.get("confidence", 1.0)  # Default full confidence
            )
            db_session.add(event)

        db_session.commit()

    except Exception as e:
        db_session.rollback()
        logger.error(f"Error saving extracted info: {e}")
