from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_type = Column(String, nullable=False)  
    target_value = Column(Integer, nullable=False, default=0)  
    deadline = Column(String, nullable=True)  
    progress = Column(Integer, nullable=True, default=0)  
    status = Column(String, nullable=True, default="Not Started")  
    unit = Column(String, nullable=False)  

    user = relationship("User", back_populates="goals")

    def __repr__(self):
        return f"<Goal(id={self.id}, user_id={self.user_id}, goal_type='{self.goal_type}', status='{self.status}')>"

    @classmethod
    def create_goal(cls, session: Session, **kwargs):
        required_fields = ["user_id", "goal_type", "target_value", "unit"]
        missing_fields = [field for field in required_fields if field not in kwargs]

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        kwargs.setdefault("progress", 0)
        kwargs.setdefault("status", "Not Started")

        goal = cls(**kwargs)
        session.add(goal)
        session.commit()
        return goal
    
    def update_goal(self, session: Session, **kwargs):
        allowed_fields = ["goal_type", "target_value", "deadline", "progress", "status", "unit"]
        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(self, key):
                setattr(self, key, value)
        
        session.commit()
        return self
    
    def delete_goal(self, session: Session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_goals_by_user_id(cls, session: Session, user_id: int):
        return session.query(cls).filter_by(user_id=user_id).all()