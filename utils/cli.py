import typer
from myapp.db import init_db

app = typer.Typer()

@app.command()
def init():
    """Initialize the database"""
    init_db()
    typer.echo("Database initialized.")

if __name__ == "__main__":
    app()