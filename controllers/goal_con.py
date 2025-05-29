from sqlalchemy.orm import Session
from models.goal import Goal


# CONTROLLERS
class GoalController:
    def __init__(self, session: Session):
        self.session = session

    def create_goal(self, **kwargs):
        goal = Goal(**kwargs)
        self.session.add(goal)
        self.session.commit()
        return goal
    
    def update_goal(self, goal_id: int, **kwargs):
        goal = self.session.query(Goal).filter_by(id=goal_id).first()
        if goal:
            for key, value in kwargs.items():
                if hasattr(goal, key):
                    setattr(goal, key, value)
            self.session.commit()
            return goal
        else:
            print(f"The Goal, {goal_id} not found.")
     
    def delete_goal(self, goal_id: int):
        goal = self.session.query(Goal).filter_by(id=goal_id).first()
        if goal:
            self.session.delete(goal)
            self.session.commit()
            return True
        return False  