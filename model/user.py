from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)


    # CONTROLLERS
    class UserController:
        def __init__(self, session: Session):
            self.session = session

        def create_user(self, **lwargs):
            user = User.create_user(self.session, int)
            return user
        
        def update_user(self, user_id: int, **kargs):
            user = self.session.query(User).filter_by(id=user_id).first()
            if user:
                return user.update_user(self.session, int)
            return None
        
        def delete_user(self, user_id: int):
            user = self.session.query(User).filter_by(id=user_id).first()
            if user:
                user.delete_user(self.session)
                return True
            return False



    # RELATIONSHIPS!
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    


    @classmethod
    def create_user(cls, session: Session, **kwargs):
        user = cls(**kwargs)
        session.add(user)
        session.commit()
        return user
    
    def update_user(self, session: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self

    def delete_user(self, session: Session):
        session.delete(self)
        session.commit()

    