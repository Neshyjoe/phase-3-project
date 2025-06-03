


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session
from models.base import Base



class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meal_type = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    carbs = Column(Integer, nullable=False)
    fats = Column(Integer, nullable=False)


    # RELATIONSHIPS
    user = relationship("User", back_populates="meal_plans")
    


    def __repr__(self):
        return f"<MealPlan(id={self.id}, user_id={self.user_id}, meal_type='{self.meal_type}')>"
    

    @classmethod
    def create_meal_plan(cls, session: Session, **kwargs):
        meal_plan = cls(**kwargs)
        session.add(meal_plan)
        session.commit()
        return meal_plan
    
    @classmethod
    def get_meal_plan_by_id(cls, session: Session, meal_plan_id: int):
        return session.query(cls).filter_by(id=meal_plan_id).first()
    
    def update_meal_plan(self, session: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self
    
    def delete_meal_plan(self, session: Session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_meal_plans_by_user_id(cls, session: Session, user_id: int):
        return session.query(cls).filter_by(user_id=user_id).all()