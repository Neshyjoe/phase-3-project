import typer
from myapp.db import init_db
from datetime import datetime
from models import SessionLocal, User, Entry, Goal, MealPlan  
from sqlalchemy.orm import sessionmaker

app = typer.Typer()
db = SessionLocal()

@app.command()
def init():
    """Initialize the database"""
    init_db()
    typer.echo("Database initialized.")


# User Commands

@app.command("user-create")
def create_user(name: str):
    user = User(name=name)
    db.add(user)
    db.commit()
    typer.echo(f" User '{name}' created successfully!")

@app.command("user-list")
def list_users():
    users = db.query(User).all()
    for user in users:
        typer.echo(f" {user.id}: {user.name}")


# Food Entry Commands

@app.command("entry-add")
def add_entry(user_id: int, food: str, calories: int, date: str):
    entry = FoodEntry(user_id=user_id, food=food, calories=calories, date=date)
    db.add(entry)
    db.commit()
    typer.echo(f" Entry added for user {user_id} on {date}")

@app.command("entry-list")
def list_entries(user_id: int = None, date: str = None):
    query = db.query(FoodEntry)
    if user_id:
        query = query.filter(FoodEntry.user_id == user_id)
    if date:
        query = query.filter(FoodEntry.date == date)
    entries = query.all()
    for e in entries:
        typer.echo(f" {e.food} - {e.calories} cal on {e.date}")

@app.command("entry-delete")
def delete_entry(id: int):
    entry = db.query(FoodEntry).get(id)
    if entry:
        db.delete(entry)
        db.commit()
        typer.echo(f" Deleted entry {id}")
    else:
        typer.echo(" Entry not found")


# Goal Commands

@app.command("goal-set")
def set_goal(user_id: int, daily: int, weekly: int):
    goal = Goal(user_id=user_id, daily=daily, weekly=weekly)
    db.add(goal)
    db.commit()
    typer.echo(" Goals set successfully")

@app.command("goal-list")
def list_goals(user_id: int):
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    for g in goals:
        typer.echo(f"Daily: {g.daily} cal, Weekly: {g.weekly} cal")


# Reporting

@app.command("report")
def report(user_id: int, date: str):
    entries = db.query(FoodEntry).filter(FoodEntry.user_id == user_id, FoodEntry.date == date).all()
    total = sum(e.calories for e in entries)
    typer.echo(f" Total calories for {date}: {total}")


# Meal Planning

@app.command("plan-meal")
def plan_meal(user_id: int, week: int):
    plan = MealPlan(user_id=user_id, week=week)
    db.add(plan)
    db.commit()
    typer.echo(f" Meal plan created for week {week}")

if __name__ == "__main__":
    app()