from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...config import load_config


conf = load_config()
engine = create_engine(conf.core.data_file, echo=True)
Session = sessionmaker(bind=engine)
