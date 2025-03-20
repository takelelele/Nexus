from sqlalchemy import URL, create_engine

import environ
from sqlalchemy.orm import declarative_base, sessionmaker

env = environ.Env()
environ.Env.read_env()

SQLALCHEMYURL = URL.create(
    drivername="postgresql+psycopg2",
    username=env("DB_USERNAME", str),
    password=env("DB_PASSWORD", str),
    host=env("DB_HOST", str),
    port=5432,
    database=env("DB_DATABASE", str)
)

engine = create_engine(SQLALCHEMYURL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()