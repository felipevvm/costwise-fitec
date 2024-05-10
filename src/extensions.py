from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
ma = Marshmallow()
af = APIFairy()
mail = Mail()