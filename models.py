from extensions import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class ParticipationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    participation_type = db.Column(db.String(50), nullable=False)  # answered/asked/involved
    activity = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)
    weather_condition = db.Column(db.String(50))