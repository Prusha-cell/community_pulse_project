from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.response import *
from app.models.question import *
from app.models.category import *
