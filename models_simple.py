import sqlite3
from datetime import datetime
import os

DB_NAME = 'matematika_test.db'

def get_db():
    """Database connection olish"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Database jadvallarini yaratish"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tests jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            image TEXT,
            class_level TEXT,
            duration_minutes INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Questions jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT NOT NULL,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (test_id) REFERENCES tests(id)
        )
    ''')
    
    # Answers jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            variant TEXT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')
    
    # Test_results jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            score REAL NOT NULL,
            correct_answers INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (test_id) REFERENCES tests(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Agar ustunlar bo'lmasa, qo'shish (mavjud database lar uchun)
    try:
        cursor.execute('ALTER TABLE tests ADD COLUMN image TEXT')
    except sqlite3.OperationalError:
        pass  # Ustun allaqachon mavjud
    try:
        cursor.execute('ALTER TABLE tests ADD COLUMN class_level TEXT')
    except sqlite3.OperationalError:
        pass  # Ustun allaqachon mavjud
    try:
        cursor.execute('ALTER TABLE tests ADD COLUMN duration_minutes INTEGER')
    except sqlite3.OperationalError:
        pass  # Ustun allaqachon mavjud
    try:
        cursor.execute('ALTER TABLE tests ADD COLUMN subject TEXT')
    except sqlite3.OperationalError:
        pass  # Ustun allaqachon mavjud
    
    conn.commit()
    conn.close()

# Database yaratish
init_db()

