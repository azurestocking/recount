from sqlalchemy import create_engine
from app.config.config import settings

def test_database_connection():
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        connection = engine.connect()
        print("Successfully connected to the database!")
        connection.close()
    except Exception as e:
        print(f"Failed to connect to the database due to: {e}")

if __name__ == "__main__":
    test_database_connection()
