import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

db_path = os.path.join(os.path.dirname(__file__), "data", "data.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
logger.info(f"Using database at: {db_path}")
logger.info(f"File exists: {os.path.exists(db_path)}")

db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    logger.info(f"Database directory created: {db_dir}")

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error in database session: {str(e)}")
        raise
    finally:
        db.close()
