


import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.goal import Goal
from controllers.goal_con import GoalController

app = typer.Typer()

DATABASE_URL = "sqlite:///./health_simplified.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Predefined valid goal types for validation
VALID_GOAL_TYPES = {"calorie-intake", "protein-consumption", "workout-frequency"}

@app.command()
def create(user_id: int, goal_type: str, target_value: float, unit: str):
    """Create a new goal with validation"""
    if goal_type.lower() not in VALID_GOAL_TYPES:
        typer.echo(f"Error: Invalid goal type '{goal_type}'. Choose from {VALID_GOAL_TYPES}.")
        return
    
    if target_value <= 0:
        typer.echo("Error: Target value must be positive.")
        return

    session = SessionLocal()
    controller = GoalController(session)

    try:
        goal = controller.create_goal(
            user_id=user_id,
            goal_type=goal_type.lower(),
            target_value=target_value,
            unit=unit
        )
        session.commit()  # Ensuring commit after creation
        typer.echo(f"Successfully created goal: {goal}")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback if there's a failure
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def update(goal_id: int, goal_type: str = None, target_value: float = None, unit: str = None, progress: str = None):
    """Update an existing goal with validation, including progress tracking"""
    session = SessionLocal()
    controller = GoalController(session)

    updates = {
        "goal_type": goal_type.lower() if goal_type else None,
        "target_value": target_value,
        "unit": unit,
        "progress": progress
    }
    updates = {k: v for k, v in updates.items() if v is not None}

    if "goal_type" in updates and updates["goal_type"] not in VALID_GOAL_TYPES:
        typer.echo(f"Error: Invalid goal type '{goal_type}'. Choose from {VALID_GOAL_TYPES}.")
        return
    
    if "target_value" in updates and updates["target_value"] <= 0:
        typer.echo("Error: Target value must be positive.")
        return

    try:
        updated_goal = controller.update_goal(goal_id, **updates)
        session.commit()  # Commit updates
        typer.echo(f"Successfully updated goal: {updated_goal}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback if error occurs
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def delete(goal_id: int):
    """Delete a goal and provide explicit confirmation"""
    session = SessionLocal()
    controller = GoalController(session)

    try:
        deleted_goal = controller.delete_goal(goal_id)
        session.commit()  # Ensure deletion is committed
        if deleted_goal:
            typer.echo(f"Successfully deleted goal ID {goal_id}.")
        else:
            typer.echo(f"Error: Goal ID {goal_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback if error occurs
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def list_goals(user_id: int):
    """List all goals for a specific user"""
    session = SessionLocal()
    controller = GoalController(session)

    try:
        goals = controller.get_goals_by_user(user_id)
        if goals:
            for goal in goals:
                typer.echo(f"ID: {goal.id} | Type: {goal.goal_type} | Target: {goal.target_value} {goal.unit} | Progress: {goal.progress}")
        else:
            typer.echo("No goals found for this user.")
    except SQLAlchemyError as e:
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    app()