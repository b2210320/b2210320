from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String,nullable=True)
    assign = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    memo = db.Column(db.Text, nullable=False)