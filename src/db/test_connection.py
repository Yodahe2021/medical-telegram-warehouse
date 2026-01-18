from sqlalchemy import text
from database import SessionLocal

def test_connection():
    # SessionLocal is the factory created in your database.py
    db = SessionLocal()
    try:
        # Test the connection
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed")
        print(f"Error details: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
