from app.models import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    question = db.relationship("Question", backref="category", lazy=True)

    def __repr__(self):
        return f'Category: {self.name}'

