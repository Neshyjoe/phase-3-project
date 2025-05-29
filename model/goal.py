from models.base import Base
from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import Session


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    goal_type = Column(String, nullable=False) 
    target_value = Column(Integer, nullable=False) 
    deadline = Column(String, nullable=True)  
    progress = Column(Integer, nullable=True) 
    status = Column(String, nullable=True) 




    def __repr__(self):
        return f"<Goal(id={self.id}, user_id={self.user_id}, goal_type='{self.goal_type}')>"
    

    @classmethod
    def create_goal(cls, session: Session, **kwargs):
        goal = cls(**kwargs)
        session.add(goal)
        session.commit()
        return goal
    
    def update_goal(self, session: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self
    
    def delete_goal(self, session: Session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_goals_by_user_id(cls, session: Session, user_id: int):
        return session.query(cls).filter_by(user_id=user_id).all()