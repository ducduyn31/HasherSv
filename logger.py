import os

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class HashedFile(Base):
    __tablename__ = 'hashed_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    extension = Column(String)
    original_hash = Column(String)
    samples = Column(Integer)
    hash_value = Column(String)
    old_hash_time = Column(BigInteger)
    new_hash_time = Column(BigInteger)
    file_size = Column(BigInteger)


saved_instances = {}


def get_session():
    if saved_instances.get('session'):
        session = saved_instances['session']
    else:
        username = 'postgres'
        password = 'mysecretpassword'
        host = 'localhost'
        port = '5432'
        database = 'postgres'

        if saved_instances.get('engine'):
            engine = saved_instances['engine']
        else:
            engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
            saved_instances['engine'] = engine

        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)

        session = Session()
        saved_instances['session'] = session

    return session


def log_to_db(file_path: str, original_hash: str, n_samples: int, new_hash: str, file_size: int, original_time: int,
              optimized_time: int):
    new_file = HashedFile(filename=os.path.basename(file_path), extension=file_path.split('.')[-1],
                          original_hash=original_hash,
                          samples=n_samples,
                          hash_value=new_hash, old_hash_time=original_time, new_hash_time=optimized_time,
                          file_size=file_size)

    get_session().add(new_file)
    get_session().commit()

    os.remove(file_path)
    return new_file