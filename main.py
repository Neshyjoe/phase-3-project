from models.base import Base
from database.engine import engine
from models.user import User
from models.goal import Goal
from models.entry import Entry
from interactive_menu import menu_selection
from database.database import get_session
from getpass import getpass  

def create_user():
    session = get_session()

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")  
    age = input("Enter your age: ")
    gender = input("Enter your gender (Male/Female): ")

    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print("Email already registered! Try logging in instead.")
        return

    new_user = User(name=name, email=email, password=password, age=age, gender=gender)
    session.add(new_user)
    session.commit()

    print(f"User {name} created successfully! You can now log in.")
    session.close()

def list_users():
    session = get_session()
    users = session.query(User).all()

    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"ID: {user.id} | Name: {user.name} | Email: {user.email}")

    session.close()
    input("\nPress Enter to return to the main menu...")  

def login_user():
    session = get_session()
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")

    user = session.query(User).filter_by(email=email).first()
    
    if user and user.password == password:
        print(f"Welcome back, {user.name}!")
        return user  
    else:
        print("Invalid email or password. Please try again.")
        return None

def user_dashboard(user):
    while True:
        print(f"\n🔹 Logged in as: {user.name}")
        print("1.View Goals")
        print("2.Set Goal")
        print("3.Delete Goal")
        print("4.View Meal Plans")
        print("5.Set Meal Plan")
        print("6.Delete Meal Plan")
        print("7.Update Personal Details")
        print("8.Logout")

        choice = input("\nSelect an option: ")

        if choice == "1":
            view_goals(user)
        elif choice == "2":
            set_goal(user)
        elif choice == "3":
            delete_goal(user)
        elif choice == "4":
            view_meal_plans(user)
        elif choice == "5":
            set_meal_plan(user)
        elif choice == "6":
            delete_meal_plan(user)
        elif choice == "7":
            update_user_details(user)
        elif choice == "8":
            print("\nLogging out...")
            break
        else:
            print("\nInvalid selection. Try again.")


def track_goal(goal, session):
    print(f"\nTracking Goal: {goal.goal_type}")
    print(f"Target: {goal.target_value} {goal.unit}")
    print(f"Current Progress: {goal.progress} {goal.unit}")
    print(f"Completion: {round((goal.progress / goal.target_value) * 100, 2)}%")
    print(f"Status: {goal.status}")
    print(f"Deadline: {goal.deadline}")

    update = input("\nEnter new progress value (or press Enter to keep current): ")
    
    if update.strip():
        try:
            new_progress = int(update)
            goal.progress = new_progress

            if new_progress == 0:
                goal.status = "Not Started"
            elif new_progress < goal.target_value:
                goal.status = "In Progress"
            else:
                goal.status = "Completed"

            session.commit()
            print(f"Updated {goal.goal_type} progress to {new_progress} {goal.unit}!")
            print(f"Status changed to: {goal.status}")

        except ValueError:
            print("Invalid input. Must be a number.")






def view_goals(user):
    session = get_session()
    goals = session.query(Goal).filter_by(user_id=user.id).all()

    if not goals:
        print("No goals found.")
        return

    print("\nYour Active Goals:")
    for index, goal in enumerate(goals, start=1):
        progress_percentage = round((goal.progress / goal.target_value) * 100, 2) if goal.target_value > 0 else 0
        print(f"{index}. {goal.goal_type}: {goal.progress}/{goal.target_value} {goal.unit} ({progress_percentage}%) - Status: {goal.status}")

    choice = input("\nEnter the number of the goal to track or press Enter to return: ")
    
    if choice.strip() == "":
        return  

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(goals):
            track_goal(goals[choice_index], session) 
        else:
            print("Invalid selection. Try again.")
    except ValueError:
        print("Invalid input. Enter a number.")

    session.close()




def set_goal(user):
    session = get_session()
    goal_type = input("Enter goal type (e.g., Calories, Steps, Weight): ")
    target_value = int(input(f"Enter target value for {goal_type}: "))
    unit = input(f"Enter unit for {goal_type} (e.g., kcal, steps, kg): ")
    deadline = input("Enter deadline (YYYY-MM-DD, optional): ")

    goal = Goal(
        user_id=user.id, 
        goal_type=goal_type, 
        target_value=target_value, 
        unit=unit,
        deadline=deadline if deadline else None
    )

    session.add(goal)
    session.commit()

    print(f"{goal_type} goal set successfully!")
    session.close()


def delete_goal(user):
    session = get_session()
    goals = session.query(Goal).filter_by(user_id=user.id).all()

    if not goals:
        print("No goals found to delete.")
        return

    print("\nSelect a goal to delete:")
    for index, goal in enumerate(goals, start=1):
        print(f"{index}. {goal.goal_type} - Target: {goal.target_value} {goal.unit} - Status: {goal.status}")

    choice = input("\nEnter the number of the goal to delete: ")
    
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(goals):
            goal_to_delete = goals[choice_index]
            session.delete(goal_to_delete)
            session.commit()
            print(f"Deleted goal: {goal_to_delete.goal_type} - {goal_to_delete.target_value} {goal_to_delete.unit}")
        else:
            print("Invalid selection. No goal deleted.")
    except ValueError:
        print("Invalid input. Enter a number.")

    session.close()


def view_meal_plans(user):
    session = get_session()
    meals = session.query(Entry).filter_by(user_id=user.id).all()

    if not meals:
        print("No meal plans found.")
    else:
        for meal in meals:
            print(f"Meal: {meal.meal} | Calories: {meal.calories} | Date: {meal.date}")

    session.close()

def set_meal_plan(user):
    session = get_session()
    meal = input("Enter meal name: ")
    calories = int(input("Enter calories: "))
    date = input("Enter date (YYYY-MM-DD): ")

    # Ensure required fields have default values
    weight = input("Enter weight (leave blank for default 60kg): ") or 60
    height = input("Enter height (leave blank for default 175cm): ") or 175
    bmi = round(float(weight) / ((float(height) / 100) ** 2), 2)

    steps = input("Enter step count (leave blank for default 0): ") or 0
    sleep_hours = input("Enter sleep hours (leave blank for default 0): ") or 0.0

    entry = Entry(
        user_id=user.id, 
        date=date, 
        weight=float(weight), 
        calories=calories, 
        height=float(height), 
        meal=meal, 
        bmi=bmi, 
        steps=int(steps), 
        sleep_hours=float(sleep_hours)
    )

    session.add(entry)
    session.commit()
    print("Meal added successfully!")
    session.close()


def delete_meal_plan(user):
    session = get_session()
    meal_plans = session.query(Entry).filter_by(user_id=user.id).all()

    if not meal_plans:
        print("No meal plans found to delete.")
        return

    print("\nSelect a meal plan to delete:")
    for index, meal in enumerate(meal_plans, start=1):
        print(f"{index}. {meal.date} - {meal.meal} | {meal.calories} kcal")

    choice = input("\nEnter the number of the meal plan to delete: ")

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(meal_plans):
            meal_to_delete = meal_plans[choice_index]
            session.delete(meal_to_delete)
            session.commit()
            print(f"Deleted meal plan: {meal_to_delete.meal} on {meal_to_delete.date}")
        else:
            print("Invalid selection. No meal deleted.")
    except ValueError:
        print("Invalid input. Enter a number.")

    session.close()


def update_user_details(user):
    session = get_session()

    new_name = input("Enter new name (leave blank to keep current): ") or user.name
    new_age = input("Enter new age (leave blank to keep current): ") or user.age
    new_weight = input("Enter new weight (leave blank to keep current): ") or user.weight
    new_height = input("Enter new height (leave blank to keep current): ") or user.height

    if hasattr(user, "weight"):
        user.weight = float(new_weight) if new_weight else user.weight
    if hasattr(user, "height"):
        user.height = float(new_height) if new_height else user.height

    user.name = new_name
    user.age = int(new_age) if new_age else user.age

    session.commit()
    print("Details updated successfully!")
    session.close()


def delete_user():
    session = get_session()
    email = input("Enter the email of the user to delete: ")

    user = session.query(User).filter_by(email=email).first()
    
    if user:
        session.delete(user)
        session.commit()
        print(f"User {user.name} deleted successfully!")
    else:
        print("User not found.")

    session.close()

def update_user():
    session = get_session()
    email = input("Enter your email: ")
    user = session.query(User).filter_by(email=email).first()

    if not user:
        print("User not found.")
        return

    print(f"Updating user: {user.name}")
    new_name = input("Enter new name (leave blank to keep current): ") or user.name
    new_password = getpass("Enter new password (leave blank to keep current): ") or user.password

    user.name = new_name
    user.password = new_password
    session.commit()

    print("User updated successfully!")
    session.close()

def main():
    while True:
        action = menu_selection()
        print(f"User selected: {action}")

        if action == "login":
            user = login_user()
            if user:
                user_dashboard(user)  

        elif action == "create":
            print("Creating a new user...")
            create_user()
        elif action == "update":
            print("Updating user information...")
            update_user()
        elif action == "delete":
            print("Deleting user...")
            delete_user()
        elif action == "list":
            print("Listing all users...")
            list_users()
        elif action == "exit":
            print("Exiting application...")
            break

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    main()