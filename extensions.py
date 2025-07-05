from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
mail = Mail()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()