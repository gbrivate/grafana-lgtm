from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ⚠️ Use a secure way to manage your credentials (e.g., environment variables)
# DO NOT hardcode sensitive data.
#SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@postgres-service.corban.svc.cluster.local:5432/mydb"
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@postgres:5432/mydb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()