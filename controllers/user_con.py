from sqlalchemy.orm import Session
from models.user import User

# CONTROLLERS
class UserController:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()
        return user
    
    def update_user(self, user_id: int, **kwargs):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
            return user
        else:
            print(f"The User, {user_id} not found.")
    
    def delete_user(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False  