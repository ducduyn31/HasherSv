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
    hashed_times = Column(Integer)


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
              hashed_time: int, optimized_time: int, remove_file_after: bool):
    existed_file = get_session().query(HashedFile).filter_by(
        filename=os.path.basename(file_path),
        extension=file_path.split('.')[-1],
        samples=n_samples,
        hash_value=new_hash,
        original_hash=original_hash
    ).first()

    if existed_file:
        old_hashed_times = existed_file.hashed_times
        new_hashed_times = old_hashed_times + hashed_time
        existed_file.hashed_times = new_hashed_times
        existed_file.new_hash_time = (
                                                 existed_file.new_hash_time * old_hashed_times + optimized_time * hashed_time) / new_hashed_times
        existed_file.old_hash_time = (
                                                 existed_file.old_hash_time * old_hashed_times + original_time * hashed_time) / new_hashed_times

        get_session().commit()
        return existed_file
    else:
        new_file = HashedFile(filename=os.path.basename(file_path), extension=file_path.split('.')[-1],
                              original_hash=original_hash,
                              samples=n_samples,
                              hash_value=new_hash, old_hash_time=original_time, new_hash_time=optimized_time,
                              hashed_times = hashed_time,
                              file_size=file_size)

        get_session().add(new_file)
        get_session().commit()

        if remove_file_after:
            os.remove(file_path)
        return new_file
