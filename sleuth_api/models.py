from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    encoded_filename = db.Column(db.String(256), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=True)
