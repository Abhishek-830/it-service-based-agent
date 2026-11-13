
from src.database.connection import engine

try:
    with engine.connect() as connection:
        result = connection.exec_driver_sql("SELECT 1")

        print("Database Connection: Successful")
        print("Test Query Result:", result.scalar())

except Exception as error:
    print("Database Connection Failed:", error)
