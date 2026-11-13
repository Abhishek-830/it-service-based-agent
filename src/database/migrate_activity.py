
from sqlalchemy import inspect

from src.database.connection import engine
from src.database.models import TicketActivity


def migrate_ticket_activity():

    inspector = inspect(engine)

    if inspector.has_table("ticket_activities"):

        print("Ticket Activity table already exists.")

    else:

        TicketActivity.__table__.create(bind=engine)

        print("Ticket Activity table created successfully.")

    print("Ticket Activity migration completed.")


if __name__ == "__main__":

    migrate_ticket_activity()
