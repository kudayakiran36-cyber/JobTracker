from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.models import *
def test_database_models():
    engine=create_engine("sqlite:///:memory:",future=True)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    with Session() as s:
        assert s.query(Job).count()==0
