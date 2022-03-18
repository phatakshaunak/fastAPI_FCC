from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# pg_password = os.environ["pg_password"]

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2 
# from psycopg2.extras import RealDictCursor
# import time
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
#                                 password = pg_password, cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break

#     except Exception as error:
#         print("Connecting to database failed with the message \n", error)
#         time.sleep(2)