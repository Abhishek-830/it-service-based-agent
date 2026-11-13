
from src.database.connection import engine, Base

# Import models
from src.database.models import Ticket


def create_database_tables():

    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_database_tables()
