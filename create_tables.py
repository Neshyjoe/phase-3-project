


from database import engine
from models.base import Base


import models.user
import models.entry
import models.goal
import models.meal_plan


Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
