from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<DB-name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/fastapiDB"

# Engine is reponsible for connecting Postgresql DB to SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()