from models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    

     # CREATE
    @classmethod
    def create_user(cls, session: Session, **kwargs):
        user = cls(**kwargs)
        session.add(user)
        session.commit()
        return user

    # READ
    @classmethod
    def get_user_by_id(cls, session: Session, user_id: int):
        return session.query(cls).filter_by(id=user_id).first()

    # UPDATE
    def update_user(self, session: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self

    # DELETE
    def delete_user(self, session: Session):
        session.delete(self)
        session.commit()

    