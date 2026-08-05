import hashlib
import uuid
from datetime import datetime

class User:
    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password_hash = self._hash(password)
        self.security_question = security_question
        self.security_answer_hash = self._hash(security_answer)
        self.failed_attempts = 0
        self.is_locked = False
        self.user_id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,            
            "security_question": self.security_question,
            "security_answer_hash": self.security_answer_hash,
            "failed_attempts": self.failed_attempts,
            "is_locked": self.is_locked,
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls.__new__(cls)
        user.username = data["username"]
        user.password_hash = data["password_hash"]
        user.security_question = data["security_question"]
        user.security_answer_hash = data["security_answer_hash"]
        user.failed_attempts = data["failed_attempts"]
        user.is_locked = data["is_locked"]
        user.user_id = data["user_id"]
        return user

        
    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()
    
    def verify_password(self, password):
        return self._hash(password) == self.password_hash
        
    def record_failed_attempt(self):
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.is_locked = True
    
    def record_successful_login(self):
        self.failed_attempts = 0
        self.is_locked = False

    def verify_security_answer(self, answer):
        return self._hash(answer) == self.security_answer_hash

class Task:
    def __init__(self, title, description, due_date, category="general"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.task_id = str(uuid.uuid4())
        self.is_completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = datetime.now().isoformat()

    def is_overdue(self):
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        return datetime.now() > due and not self.is_completed

    def is_urgent(self):
        if self.is_completed:
            return False
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        days_left = (due - datetime.now()).days
        return days_left >= 0 and days_left <= 3

    def days_until_due(self):
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        days_left = (due - datetime.now()).days
        return days_left

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "category": self.category,
            "task_id": self.task_id,
            "is_completed": self.is_completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls,data):
        task = cls.__new__(cls)
        task.title = data["title"]
        task.description = data["description"]
        task.due_date = data["due_date"]
        task.category = data["category"]
        task.task_id = data["task_id"]
        task.is_completed = data["is_completed"]
        task.created_at = data["created_at"]
        task.completed_at = data["completed_at"]
        return task
