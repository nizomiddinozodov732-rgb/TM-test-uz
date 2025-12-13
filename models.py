from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Foydalanuvchi modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Test(db.Model):
    """Test modeli"""
    __tablename__ = 'tests'
    
    id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Test {self.name}>'

class Question(db.Model):
    """Savol modeli"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.String(6), db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, yoki D
    
    def __repr__(self):
        return f'<Question {self.id}>'

class Answer(db.Model):
    """Javob variantlari modeli"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    variant = db.Column(db.String(1), nullable=False)  # A, B, C, yoki D
    text = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Answer {self.variant}>'

class TestResult(db.Model):
    """Test natijalari modeli"""
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.String(6), db.ForeignKey('tests.id'), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # Foizda
    correct_answers = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestResult {self.id}>'


