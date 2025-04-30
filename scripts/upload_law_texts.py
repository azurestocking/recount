import uuid
from app.models.database import Law, SessionLocal
from app.services.faiss_connector import save_law_embedding, load_faiss_index, load_law_ids, LAW_INDEX_ID
from app.services.generate_law_related_ids import generate_law_related_ids

def upload_law_texts(law_text_list: list):
    """
    Upload a batch of law descriptions into the database and FAISS, then update related_ids.
    :param law_text_list: List[str] of law descriptions.
    """
    session = SessionLocal()

    try:
        # 1. Insert into Law table
        new_ids = []
        for description in law_text_list:
            new_id = str(uuid.uuid4())
            law_record = Law(
                id=new_id,
                conversation_id=None,
                type="law",
                file_path="",
                description=description,
                metadata={}
            )
            session.add(law_record)
            new_ids.append(new_id)

        session.commit()
        print(f"✅ Inserted {len(new_ids)} laws into database.")

        # 2. Insert into FAISS
        for law_id in new_ids:
            law = session.query(Law).filter(Law.id == law_id).first()
            if law and law.description:
                save_law_embedding(session, law_id, law.description)
        print(f"✅ Embedded {len(new_ids)} laws into FAISS.")

        # 3. Reload FAISS index
        law_index = load_faiss_index(session, LAW_INDEX_ID, 1536)

        # 4. Refresh global law_ids cache
        load_law_ids(session)

        # 5. Generate related_ids
        from app.services.faiss_connector import law_ids  # lazy import after refresh
        generate_law_related_ids(session, law_index, law_ids, max_neighbors=3)
        print(f"✅ Updated related_ids for laws.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error uploading law texts: {str(e)}")
    finally:
        session.close()
