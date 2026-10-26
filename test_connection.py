
from sqlalchemy import text
from python.db_config import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM analytics.sales_clean")
        )
        print("Database connection successful!")
        print("Rows in sales_clean:", result.scalar())

except Exception as error:
    print("Database connection failed.")
    print(type(error).__name__, error)
