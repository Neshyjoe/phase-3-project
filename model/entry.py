from models.base import Base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey, Float

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    height = Column(Float, nullable=False)
    meal = Column(String, nullable=True)
    bmi = Column(Float, nullable=False)
    steps = Column(Integer, nullable=True)
    sleep_hours = Column(Float, nullable=True)

    user = relationship("User", back_populates="entries")

    def __repr__(self):
        return f"<Entry(id={self.id}, user_id={self.user_id}, date='{self.date}')>"
    
    @classmethod
    def create_with_fallback(cls, session: Session, user_id, date, weight=None, calories=None, height=None, bmi=None, steps=None, sleep_hours=None, meal=None):
        weight = weight if weight is not None else 60.0
        height = height if height is not None else 179.0
        bmi = bmi if bmi is not None else round(weight / ((height / 100) ** 2), 2)
        steps = steps if steps is not None else 0
        sleep_hours = sleep_hours if sleep_hours is not None else 0.0
        meal = meal if meal is not None else "No meal recorded"

        entry = cls(
            user_id=user_id,
            date=date,
            weight=weight,
            calories=calories,
            height=height,
            bmi=bmi,
            steps=steps,
            sleep_hours=sleep_hours,
            meal=meal
        )
        session.add(entry)
        session.commit()
        return entry

    @classmethod
    def create_entry(cls, session: Session, **kwargs):
        required_fields = ["user_id", "date", "weight", "height", "bmi"]
        missing_fields = [field for field in required_fields if field not in kwargs]

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        kwargs.setdefault("steps", 0)
        kwargs.setdefault("sleep_hours", 0.0)
        kwargs.setdefault("meal", "No meal recorded")

        entry = cls(**kwargs)
        session.add(entry)
        session.commit()
        return entry

    def update_entry(self, session: Session, **kwargs):
        allowed_fields = ["weight", "calories", "height", "bmi", "steps", "sleep_hours", "meal"]
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        
        session.commit()
        return self

    def delete_entry(self, session: Session):
        session.delete(self)
        session.commit()