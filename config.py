
import os
from dotenv import load_dotenv

load_dotenv('s.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mansnothot')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:saleemmz:mansnothot@localhost/SPT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
    SMTP_PORT = os.getenv('SMTP_PORT', 587)
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'saleemm1137@gmail.com')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'ktcttcuzfzleiyto')
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'SPT <saleemm1137@gmail.com>')
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_FROM', 'SPT <saleemm1137@gmail.com>')
    