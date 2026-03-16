from extensions import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed


class ParticipationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    weather_condition = db.Column(db.String(50))  # New column
    timestamp = db.Column(db.DateTime, default=db.func.now())