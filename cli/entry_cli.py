


import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.entry import Entry
from controllers.entry_con import EntryController

app = typer.Typer()

DATABASE_URL = "sqlite:///./health_simplified.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

@app.command()
def create(user_id: int, date: str, meal: str, calories: int):
    """Create a new entry with input validation"""
    if calories < 0:
        typer.echo("Error: Calories must be a non-negative value.")
        return

    session = SessionLocal()
    controller = EntryController(session)

    try:
        entry = controller.create_entry(user_id=user_id, date=date, meal=meal, calories=calories)
        session.commit()  # Commit only if successful
        typer.echo(f"Successfully created entry: {entry}")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of failure
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def update(entry_id: int, user_id: int = None, date: str = None, meal: str = None, calories: int = None):
    """Update an entry with validation"""
    session = SessionLocal()
    controller = EntryController(session)

    updates = {k: v for k, v in {"user_id": user_id, "date": date, "meal": meal, "calories": calories}.items() if v is not None}

    if "calories" in updates and updates["calories"] < 0:
        typer.echo("Error: Calories must be a non-negative value.")
        return

    try:
        updated_entry = controller.update_entry(entry_id, **updates)
        session.commit()  # Commit successful updates
        typer.echo(f"Successfully updated entry: {updated_entry}")
    except ValueError as e:
        session.rollback()
        typer.echo(f"Error: {e}")
    except SQLAlchemyError as e:
        session.rollback()
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def delete(entry_id: int):
    """Delete an entry and provide explicit confirmation"""
    session = SessionLocal()
    controller = EntryController(session)

    try:
        deleted_entry = controller.delete_entry(entry_id)
        session.commit()  # Ensure deletion is committed
        if deleted_entry:
            typer.echo(f"Successfully deleted entry ID {entry_id}.")
        else:
            typer.echo(f"Error: Entry ID {entry_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def list_entries(user_id: int):
    """List all entries for a specific user"""
    session = SessionLocal()
    controller = EntryController(session)

    try:
        entries = controller.get_entries_by_user(user_id)
        if entries:
            for entry in entries:
                typer.echo(f"ID: {entry.id} | Date: {entry.date} | Meal: {entry.meal} | Calories: {entry.calories}")
        else:
            typer.echo("No entries found for this user.")
    except SQLAlchemyError as e:
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    app()