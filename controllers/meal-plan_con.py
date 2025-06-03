


from sqlalchemy.orm import Session
from models.meal_plan import MealPlan

class MealPlanController:
    def __init__(self, session: Session):
        self.session = session

    def create_meal_plan(self, **kwargs):
        """Create a new meal plan with validation"""
        valid_meal_types = {"breakfast", "lunch", "dinner", "snack"}

        if "meal_type" in kwargs and kwargs["meal_type"].lower() not in valid_meal_types:
            raise ValueError(f"Invalid meal type '{kwargs['meal_type']}'. Allowed values: {valid_meal_types}")

        for key in ["calories", "protein", "carbs", "fats"]:
            if kwargs.get(key) is not None and kwargs[key] < 0:
                raise ValueError(f"{key} cannot be negative.")

        meal_plan = MealPlan(**kwargs)
        self.session.add(meal_plan)
        self.session.commit()
        return meal_plan

    def update_meal_plan(self, meal_plan_id: int, **kwargs):
        """Update an existing meal plan with field validation"""
        allowed_fields = {"meal_type", "calories", "protein", "carbs", "fats"}
        valid_meal_types = {"breakfast", "lunch", "dinner", "snack"}

        meal_plan = self.session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if not meal_plan:
            raise ValueError(f"Meal plan with id {meal_plan_id} not found.")

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                if key == "meal_type" and value.lower() not in valid_meal_types:
                    raise ValueError(f"Invalid meal type '{value}'. Allowed values: {valid_meal_types}")
                if key in {"calories", "protein", "carbs", "fats"} and value < 0:
                    raise ValueError(f"{key} cannot be negative.")
                setattr(meal_plan, key, value)

        self.session.commit()
        return meal_plan

    def delete_meal_plan(self, meal_plan_id: int):
        """Delete a meal plan and provide explicit confirmation"""
        meal_plan = self.session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if not meal_plan:
            raise ValueError(f"Meal plan ID {meal_plan_id} not found.")

        self.session.delete(meal_plan)
        self.session.commit()
        return f"Successfully deleted meal plan ID {meal_plan_id}."





