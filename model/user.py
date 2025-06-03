from models.base import Base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Integer, String, Float
from models.entry import Entry
from models.goal import Goal
from models.meal_plan import MealPlan

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=True, default=18)  
    weight = Column(Float, nullable=True, default=60.0)  
    height = Column(Float, nullable=True, default=175.0)  
    bmi = Column(Float, nullable=True)  
    gender = Column(String, nullable=True)  

    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan", lazy="selectin", single_parent=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    @classmethod
    def create_user(cls, session: Session, **kwargs):
        required_fields = ["name", "email", "password"]
        missing_fields = [field for field in required_fields if field not in kwargs]

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Set default values for optional fields
        kwargs.setdefault("age", 18)
        kwargs.setdefault("weight", 60.0)
        kwargs.setdefault("height", 175.0)
        kwargs.setdefault("gender", "Not specified")

        # Calculate BMI dynamically if weight and height exist
        if kwargs["weight"] and kwargs["height"]:
            kwargs["bmi"] = round(kwargs["weight"] / ((kwargs["height"] / 100) ** 2), 2)

        user = cls(**kwargs)
        session.add(user)
        session.commit()
        return user
    
    def update_user(self, session: Session, **kwargs):
        allowed_fields = ["name", "password", "age", "weight", "height", "bmi", "gender"]
        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(self, key):
                setattr(self, key, value)
        
        session.commit()
        return self

    def delete_user(self, session: Session):
        session.delete(self)
        session.commit()