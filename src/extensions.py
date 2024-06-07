from apifairy import APIFairy
from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
af = APIFairy()
mail = Mail()
cors = CORS()
