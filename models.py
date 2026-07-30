import hashlib

class User:
    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password_hash = self._hash(password)
        self.security_question = security_question
        self.security_answer_hash = self._hash(security_answer)
        self.failed_attempts = 0
        self.is_locked = False
        
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