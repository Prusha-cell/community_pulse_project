from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.responses import *
from app.models.questions import *
from app.models.category import *
