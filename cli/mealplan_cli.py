


import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.meal_plan import MealPlan
from controllers.meal_plan_con import MealPlanController

app = typer.Typer()

# Setup DB session
DATABASE_URL = "sqlite:///./health_simplified.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Predefined meal types for validation
VALID_MEAL_TYPES = {"breakfast", "lunch", "dinner", "snack"}

@app.command()
def create(
    user_id: int,
    meal_type: str,
    calories: int,
    protein: int,
    carbs: int,
    fats: int
):
    """Create a new meal plan with input validation"""
    if meal_type.lower() not in VALID_MEAL_TYPES:
        typer.echo(f"Error: Invalid meal type '{meal_type}'. Choose from {VALID_MEAL_TYPES}.")
        return

    if any(val < 0 for val in [calories, protein, carbs, fats]):
        typer.echo("Error: Calories, protein, carbs, and fats must be non-negative values.")
        return

    session = SessionLocal()
    controller = MealPlanController(session)

    try:
        meal_plan = controller.create_meal_plan(
            user_id=user_id,
            meal_type=meal_type.lower(),
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
        typer.echo(f"Successfully created meal plan: {meal_plan}")
    except SQLAlchemyError as e:
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def update(
    meal_plan_id: int,
    meal_type: str = None,
    calories: int = None,
    protein: int = None,
    carbs: int = None,
    fats: int = None
):
    """Update an existing meal plan with validation"""
    session = SessionLocal()
    controller = MealPlanController(session)

    updates = {
        "meal_type": meal_type.lower() if meal_type else None,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fats": fats
    }
    updates = {k: v for k, v in updates.items() if v is not None}

    if "meal_type" in updates and updates["meal_type"] not in VALID_MEAL_TYPES:
        typer.echo(f"Error: Invalid meal type '{meal_type}'. Choose from {VALID_MEAL_TYPES}.")
        return
    
    if any(val < 0 for key, val in updates.items() if key in {"calories", "protein", "carbs", "fats"}):
        typer.echo("Error: Calories, protein, carbs, and fats must be non-negative values.")
        return

    try:
        updated_plan = controller.update_meal_plan(meal_plan_id, **updates)
        typer.echo(f"Successfully updated meal plan: {updated_plan}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    except SQLAlchemyError as e:
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

@app.command()
def delete(meal_plan_id: int):
    """Delete a meal plan and provide explicit confirmation"""
    session = SessionLocal()
    controller = MealPlanController(session)

    try:
        deleted_plan = controller.delete_meal_plan(meal_plan_id)
        if deleted_plan:
            typer.echo(f"Successfully deleted meal plan ID {meal_plan_id}.")
        else:
            typer.echo(f"Error: Meal plan ID {meal_plan_id} not found.")
    except SQLAlchemyError as e:
        typer.echo(f"Database error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    app()