from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...config import load_config


conf = load_config()
engine = create_engine(conf.core.data_file, echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_sql_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
