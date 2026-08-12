import os
import json

def get_file_path(username):
    """
    Build a path to the users JSON file
    Example: get_file_path("Ramzaan") returns data/Ramzaan.json
    """
    return os.path.join("data", f"{username}.json")

def check_data():
    """ 
    Check if an existing data file already exists
    If not then create a new one
    """
    if not os.path.exists("data"): # check
        os.makedirs("data") # creating the folder

def save_data(username,data):
    """
    Saving user data to the JSON file

    args:
        username: string eg "Ramzaan"
        data: dictionary with user info and tasks
    """
    check_data() # does the file exist 
    file_path = get_file_path(username) # build the path
    with open(file_path, "w") as file:
        json.dump(data,file, indent=4)

def load_data(username):
    """
    Load user data from JSON file
    Returns the dictionary or None if the file doesnt exist
    """
    file_path = get_file_path(username)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return json.load(file)