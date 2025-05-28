from models.base import Base
from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import Session


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=True)
    height = Column(Integer, nullable=False)
    bmi = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=True)
    sleep_hours = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Entry(id={self.id}, user_id={self.user_id}, date='{self.date}')>"
    

 # CREATE
    @classmethod
    def create_entry(cls, session: Session, **kwargs):
        entry = cls(**kwargs)
        session.add(entry)
        session.commit()
        return entry

 # READ
    @classmethod
    def get_entry_by_id(cls, session: Session, entry_id: int):
        return session.query(cls).filter_by(id=entry_id).first()

 # UPDATE
    def update_entry(self, session: Session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self

 # DELETE
    def delete_entry(self, session: Session):
        session.delete(self)
        session.commit()