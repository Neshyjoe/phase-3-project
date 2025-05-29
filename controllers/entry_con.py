from sqlalchemy.orm import Session
from models.entry import Entry


# CONTROLLERS
class EntryController:
    def __init__(self, session: Session):
        self.session = session

    def create_entry(self, **kwargs):
        entry = Entry(**kwargs)
        self.session.add(entry)
        self.session.commit()
        return entry
    
    def update_entry(self, entry_id: int, **kwargs):
        entry = self.session.query(Entry).filter_by(id=entry_id).first()
        if entry:
            for key, value in kwargs.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            self.session.commit()
            return entry
        else:
            print(f"The Entry, {entry_id} not found.")
    
    def delete_entry(self, entry_id: int):
        entry = self.session.query(Entry).filter_by(id=entry_id).first()
        if entry:
            self.session.delete(entry)
            self.session.commit()
            return True
        return False  