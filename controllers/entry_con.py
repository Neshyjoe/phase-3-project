


from sqlalchemy.orm import Session
from models.entry import Entry


# CONTROLLERS
class EntryController:
    def __init__(self, session: Session):
        self.session = session

    def get_entries_by_user(self, user_id):
        """Retrieve all entries for a specific user"""
        return self.session.query(Entry).filter_by(user_id=user_id).all()

    def create_entry(self, **kwargs):
        """Create a new entry with validation"""
        for key in ["weight", "calories", "height", "bmi", "steps", "sleep_hours"]:
            if kwargs.get(key) is not None and kwargs[key] < 0:
                raise ValueError(f"{key} cannot be negative.")

        entry = Entry(**kwargs)
        self.session.add(entry)
        self.session.commit()
        return entry

    
    def update_entry(self, entry_id: int, **kwargs):
        """Update entry with field validation"""
        allowed_fields = {"weight", "calories", "height", "bmi", "steps", "sleep_hours", "meal"}

        entry = self.session.query(Entry).filter_by(id=entry_id).first()
        if not entry:
            raise ValueError(f"Entry with id {entry_id} not found.")

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                if key in {"weight", "calories", "height", "bmi", "steps", "sleep_hours"} and value < 0:
                    raise ValueError(f"{key} cannot be negative.")
                setattr(entry, key, value)

        self.session.commit()
        return entry

    
    def delete_entry(self, entry_id: int):
        """Delete an entry and provide explicit confirmation"""
        entry = self.session.query(Entry).filter_by(id=entry_id).first()
        if not entry:
            raise ValueError(f"Entry ID {entry_id} not found.")

        self.session.delete(entry)
        self.session.commit()
        return f"Successfully deleted entry ID {entry_id}."
