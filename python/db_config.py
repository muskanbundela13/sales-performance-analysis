
import os
from sqlalchemy import create_engine

DB_USER = os.getenv("PGUSER", "postgres")
DB_PASSWORD = os.environ["PGPASSWORD"]
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
DB_NAME = "sales_performance_db"

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
