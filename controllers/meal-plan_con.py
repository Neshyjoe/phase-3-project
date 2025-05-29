from sqlalchemy.orm import Session
from models.meal_plan import Mealplan


# CONTROLLERS
class MealPlanController:
    def __init__(self, session: Session):
        self.session = session

    def create_meal_plan(self, **kwargs):
        meal_plan = Meal_Plan(**kwargs)
        self.session.add(meal_plan)
        self.session.commit()
        return meal_plan
    
    def update_meal_plan(self, meal_plan_id: int, **kwargs):
        meal_plan = self.session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if meal_plan:
            for key, value in kwargs.items():
                if hasattr(meal_plan, key):
                    setattr(meal_plan, key, value)
            self.session.commit()
            return meal_plan
        else:
            print(f"Meal plan with ID {meal_plan_id} not found.")
    
    def delete_meal_plan(self, meal_plan_id: int):
        meal_plan = self.session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if meal_plan:
            self.session.delete(meal_plan)
            self.session.commit()
            return True
        return False