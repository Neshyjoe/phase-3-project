


from sqlalchemy.orm import Session
from models.user import User
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Custom Exceptions
class UserNotFoundError(Exception):
    pass

class DuplicateUserError(Exception):
    pass

# CONTROLLER
class UserController:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, **kwargs):
        """Create a new user with email validation and password hashing"""
        existing_user = self.session.query(User).filter_by(email=kwargs.get("email")).first()
        if existing_user:
            raise DuplicateUserError(f"User with email {kwargs.get('email')} already exists.")
        
        # Hash password before saving
        if "password" in kwargs:
            kwargs["password"] = pwd_context.hash(kwargs["password"])
        
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()
        return user
    
    def update_user(self, user_id: int, **kwargs):
        """Update user details with restricted fields validation"""
        allowed_fields = {"name", "email", "age", "gender"}  # Prevent sensitive changes

        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found.")

        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)

        self.session.commit()
        return user

    def delete_user(self, user_id: int):
        """Delete a user and provide clear feedback"""
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found.")
        
        self.session.delete(user)
        self.session.commit()
        return f" User {user.name} deleted successfully."
