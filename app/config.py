import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

class config:
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRESQL_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    MAX_CONTENT_LENGTH= 50*1024*1024
    JWT_SECRET_KEY = "test-secret"
    JWT_VERIFY_SUB = False
     



    
