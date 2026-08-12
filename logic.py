from models import User, Task
import storage

def register_user(username, password, security_question, security_answer):
    # User check
    existing_user = storage.load_data(username)
    if existing_user is not None:
        return False  # Username taken

    # Create new user
    new_user = User(username, password, security_question, security_answer)
    user_dict = new_user.to_dict()

    # Save to JSON
    storage.save_data(username, user_dict)
    return True  # Registration successful


def login_user(username, password):
    # Load user data from file
    existing_user = storage.load_data(username)
    if existing_user is None:
        return False  # User not found

    # Rebuild User object so we can use its methods
    user = User.from_dict(existing_user)

    # Check if account is locked
    if user.is_locked:
        return "Locked"

    # Password Check
    if user.verify_password(password):
        # Correct password - reset failed attempts and unlock
        user.record_successful_login()
        user_dict = user.to_dict()
        storage.save_data(username, user_dict)
        return True  # Login successful
    else:
        # Wrong password, failed attempts
        user.record_failed_attempt()
        user_dict = user.to_dict()
        storage.save_data(username, user_dict)
        return "wrong password"


def add_task(username, title, description, due_date, category="general"):
    # Load user data
    data = storage.load_data(username)
    
    # Create tasks list if it doesnt exist
    if "tasks" not in data:
        data["tasks"] = []
    
    # Create task, convert to dict, add to list, save
    task = Task(title, description, due_date, category)
    task_dict = task.to_dict()
    data["tasks"].append(task_dict)
    storage.save_data(username, data)