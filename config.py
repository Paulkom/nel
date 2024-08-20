import os
# from dotenv import load_dotenv

# load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/nel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
