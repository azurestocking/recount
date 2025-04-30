# from scripts.upload_law_texts import upload_law_texts
#
# if __name__ == "__main__":
#     laws = [
#         "The tenant shall not sublet the premises without prior written consent.",
#         "Employees must report harassment incidents to the HR department within 30 days.",
#         "The warranty period shall be two years from the date of purchase.",
#         "Minors under 18 are prohibited from entering the establishment after 10 PM.",
#         "All vehicles must comply with the emissions standards set by the Environmental Agency."
#     ]
#
#     upload_law_texts(laws)

from app.models.database import SessionLocal
from app.models.database import Law
from app.services.faiss_connector import save_law_embedding

import uuid

def upload_laws():
    session = SessionLocal()
    law_texts = [
        "The tenant shall not sublet the premises without prior written consent.",
        "Employees must report harassment incidents to the HR department within 30 days.",
        "The warranty period shall be two years from the date of purchase.",
        "Minors under 18 are prohibited from entering the establishment after 10 PM.",
        "All vehicles must comply with the emissions standards set by the Environmental Agency."
    ]
    try:
        for text in law_texts:
            new_id = str(uuid.uuid4())
            law_record = Law(
                id=new_id,
                conversation_id=None,
                type="law",
                file_path="",
                description=text,
                metadata={}
            )
            session.add(law_record)
            session.commit()

            save_law_embedding(session, new_id, text)

        from app.services.faiss_connector import load_law_ids
        load_law_ids(session)

        print(f"✅ Inserted and embedded {len(law_texts)} laws.")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to upload laws: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    upload_laws()

