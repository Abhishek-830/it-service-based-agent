
from sqlalchemy import inspect, text

from src.database.connection import engine


def migrate_handoff_columns():

    inspector = inspect(engine)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("tickets")
    }

    migrations = {
        "assigned_to": (
            "ALTER TABLE tickets "
            "ADD COLUMN assigned_to VARCHAR(100)"
        ),

        "escalation_reason": (
            "ALTER TABLE tickets "
            "ADD COLUMN escalation_reason TEXT"
        ),

        "handoff_status": (
            "ALTER TABLE tickets "
            "ADD COLUMN handoff_status "
            "VARCHAR(30) NOT NULL DEFAULT 'Pending'"
        )
    }

    with engine.begin() as connection:

        for column_name, migration_sql in migrations.items():

            if column_name not in existing_columns:

                connection.execute(text(migration_sql))

                print(f"Added column: {column_name}")

            else:

                print(f"Already exists: {column_name}")

    print("Human Support Handoff migration completed.")


if __name__ == "__main__":
    migrate_handoff_columns()
