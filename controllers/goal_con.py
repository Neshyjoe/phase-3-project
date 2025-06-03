


from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from models.goal import Goal

# Custom Exceptions
class GoalNotFoundError(Exception):
    pass

class GoalController:
    def __init__(self, session: Session):
        self.session = session

    def get_goals_by_user(self, user_id):
        """Retrieve all goals for a specific user using parameterized query"""
        try:
            query = text("SELECT * FROM goals WHERE user_id = :user_id")
            result = self.session.execute(query, {"user_id": user_id}).fetchall()
            return result
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {e}")

    def create_goal(self, **kwargs):
        """Create a new goal with validation & parameterized query"""
        valid_goal_types = {"calorie-intake", "protein-consumption", "workout-frequency"}

        if "goal_type" in kwargs and kwargs["goal_type"].lower() not in valid_goal_types:
            raise ValueError(f"Invalid goal type '{kwargs['goal_type']}'. Allowed values: {valid_goal_types}")

        if "target_value" in kwargs and kwargs["target_value"] <= 0:
            raise ValueError("Target value must be positive.")

        try:
            goal = Goal(**kwargs)
            self.session.add(goal)
            self.session.commit()
            return goal
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Database error: {e}")

    def update_goal(self, goal_id: int, **kwargs):
        """Update an existing goal with validation & secure queries"""
        allowed_fields = {"goal_type", "target_value", "deadline", "progress", "status"}
        valid_goal_types = {"calorie-intake", "protein-consumption", "workout-frequency"}

        goal = self.session.query(Goal).filter_by(id=goal_id).first()
        if not goal:
            raise GoalNotFoundError(f"Goal with id {goal_id} not found.")

        try:
            for key, value in kwargs.items():
                if key in allowed_fields and value is not None:
                    if key == "goal_type" and value.lower() not in valid_goal_types:
                        raise ValueError(f"Invalid goal type '{value}'. Allowed values: {valid_goal_types}")
                    if key == "target_value" and value <= 0:
                        raise ValueError("Target value must be positive.")
                    setattr(goal, key, value)

            self.session.commit()
            return goal
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Database error: {e}")

    def delete_goal(self, goal_id: int):
        """Delete a goal safely with rollback in case of failure"""
        goal = self.session.query(Goal).filter_by(id=goal_id).first()
        if not goal:
            raise GoalNotFoundError(f"Goal ID {goal_id} not found.")

        try:
            self.session.delete(goal)
            self.session.commit()
            return f"Successfully deleted goal ID {goal_id}."
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Database error: {e}")