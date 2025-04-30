from app.models.database import SessionLocal
from app.models.database import Evidence
from app.services.faiss_connector import save_evidence_embedding

import uuid

def upload_evidences():
    session = SessionLocal()
    evidence_texts = [
        "Evidence: Email about the contract.",
        "Evidence: Witness report regarding incident.",
        "Evidence: CCTV footage description.",
        "Evidence: Police report statement.",
        "Evidence: Photograph of the scene."
    ]
    try:
        for text in evidence_texts:
            new_id = str(uuid.uuid4())
            evidence_record = Evidence(
                id=new_id,
                conversation_id=None,
                type="evidence",
                file_path="",
                description=text,
                metadata={}
            )
            session.add(evidence_record)
            session.commit()

            save_evidence_embedding(session, new_id, text)

        from app.services.faiss_connector import load_evidence_ids
        load_evidence_ids(session)

        print(f"✅ Inserted and embedded {len(evidence_texts)} evidences.")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to upload evidences: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    upload_evidences()



# if __name__ == "__main__":
#     # ✍️ 这里是你想上传的证据文本！
#     evidences = [
#         "Surveillance footage from parking lot camera.",
#         "Medical report dated January 15, 2023.",
#         "Witness statement from John Doe.",
#         "Email correspondence regarding the incident.",
#         "Photograph of the injury site."
#     ]
#
#     upload_evidence_texts(evidences)
