from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .config import settings


load_dotenv()


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host=os.getenv("POSTGRES_HOST"),
#             database=os.getenv("POSTGRES_DATABASE"),
#             user=os.getenv("POSTGRES_USER"),
#             password=os.getenv("POSTGRES_PASSWORD"),
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         two_seconds = 2
#         time.sleep(two_seconds)
