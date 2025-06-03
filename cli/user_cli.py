import typer
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from controllers.user_con import UserController
from database.database import get_session
from utils.current_user import set_current_user, get_current_user, clear_current_user
from cli import goal_cli, entry_cli


app = typer.Typer()
app.add_typer(goal_cli.app, name="goal")
app.add_typer(entry_cli.app, name="entry")

@app.command()
def create(name: str, email: str, password: str, age: int, gender: str):
    """Create a new user with validation and password hashing"""
    session = get_session()
    controller = UserController(session)

    try:
        user = controller.create_user(name=name, email=email, password=password, age=age, gender=gender)
        typer.echo(f"User created successfully: {user}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    except SQLAlchemyError:
        typer.echo("Database error occurred while creating the user.")
    finally:
        session.close()

@app.command()
def update(user_id: int, name: str = None, email: str = None, password: str = None, age: int = None, gender: str = None):
    """Update user information with validation"""
    session = get_session()
    controller = UserController(session)
    kwargs = {k: v for k, v in {"name": name, "email": email, "password": password, "age": age, "gender": gender}.items() if v is not None}

    try:
        user = controller.update_user(user_id, **kwargs)
        typer.echo(f"User updated successfully: {user}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    except SQLAlchemyError:
        typer.echo("Database error occurred while updating the user.")
    finally:
        session.close()

@app.command()
def delete(user_id: int):
    """Delete a user and provide explicit confirmation"""
    session = get_session()
    controller = UserController(session)

    try:
        success = controller.delete_user(user_id)
        if success:
            typer.echo(f"User ID {user_id} deleted successfully.")
        else:
            typer.echo(f"Error: User ID {user_id} not found.")
    except SQLAlchemyError:
        typer.echo("Database error occurred while deleting the user.")
    finally:
        session.close()

@app.command()
def login(user_id: int):
    """Log in as an existing user"""
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()

    if user:
        set_current_user(user_id)
        typer.echo(f"Logged in as: {user.name} (ID: {user.id})")
    else:
        typer.echo("Error: User not found.")
    
    session.close()

@app.command()
def logout():
    """Log out the current user"""
    clear_current_user()
    typer.echo("Successfully logged out.")

@app.command()
def whoami():
    """Display the currently logged-in user"""
    user_id = get_current_user()
    
    if user_id:
        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            typer.echo(f"Currently logged in as: {user.name} (ID: {user.id})")
        else:
            typer.echo("Session exists, but user not found.")
        session.close()
    else:
        typer.echo("No user is currently logged in.")

@app.command()
def list_users():
    """List all registered users"""
    session = get_session()
    users = session.query(User).all()

    if users:
        for user in users:
            typer.echo(f"ID: {user.id} | Name: {user.name} | Email: {user.email}")
    else:
        typer.echo("No users found.")

    session.close()

if __name__ == "__main__":
    app()