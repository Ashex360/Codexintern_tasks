import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLite database file inside "instance" folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for session & JWT
    SECRET_KEY = "supersecretkey"  
    JWT_SECRET_KEY = "jwt-secret-string"  # used by flask-jwt-extended
