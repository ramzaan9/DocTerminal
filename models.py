import uuid
from datetime import datetime

class Task:
    """Represents a single task/assignment"""
    def __init__(self, title, description, due_date, category="general"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.task_id = str(uuid.uuid4()) # Task Identifier
        self.is_completed = False # Defaulted at Not Complete
        self.created_at = datetime.now().isoformat()
        self.completed_at = None # Filled when marked as Complete

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = datetime.now().isoformat()

    def is_overdue(self):
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return datetime.now().date() > due_date and not self.is_completed

    def is_urgent(self):
        if self.is_completed:
            return False
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        days_left = (due_date - datetime.now().date()).days
        return 0 <= days_left <= 3

    def days_until_due(self):
        """Return number of days until deadline, negative if overdue"""
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return (due_date - datetime.now().date()).days

    def to_dict(self):
        """Convert Task object to dictionary for JSON storage"""
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
    def from_dict(cls, data):
        """Rebuild Task object from a dictionary"""
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