from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from extensions import db
from weather import get_weather
from datetime import date

# ----------------------
# App Configuration
# ----------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ----------------------
# Weather Label Mapping
# ----------------------
WEATHER_LABEL_MAP = {
    'Clear':        'Sunny',
    'Clouds':       'Cloudy',
    'Rain':         'Rainy',
    'Drizzle':      'Rainy',
    'Thunderstorm': 'Rainy',
    'Snow':         'Windy',
    'Wind':         'Windy',
    'Mist':         'Cloudy',
    'Fog':          'Cloudy',
    'Haze':         'Cloudy',
}

# ----------------------
# Models
# ----------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class ParticipationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    activity = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)
    weather_condition = db.Column(db.String(50))

# ----------------------
# User Loader
# ----------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------------
# Initialize Database
# ----------------------
with app.app_context():
    db.create_all()
    if not Student.query.first():
        db.session.add_all([Student(name="Alice"), Student(name="Bob")])
        db.session.commit()

# ----------------------
# Routes
# ----------------------
@app.route('/')
@login_required
def index():
    logs = ParticipationLog.query.all()
    log_list = []
    for log in logs:
        student = Student.query.get(log.student_id)
        log_list.append({
            "student_name": student.name if student else "Unknown",
            "activity": log.activity,
            "date": log.date,
            "weather_condition": log.weather_condition
        })

    # Always show all 4 categories, starting at 0
    weather_counts = {'Sunny': 0, 'Cloudy': 0, 'Rainy': 0, 'Windy': 0}
    for log in logs:
        raw = log.weather_condition or 'Unknown'
        normalized = WEATHER_LABEL_MAP.get(raw, 'Cloudy')
        weather_counts[normalized] += 1

    weather_labels = list(weather_counts.keys())
    activity_counts = list(weather_counts.values())

    return render_template(
        "index.html",
        logs=log_list,
        weather_labels=weather_labels,
        activity_counts=activity_counts
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/log', methods=['GET', 'POST'])
@login_required
def log_participation():
    students = Student.query.all()
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        activity = request.form.get('activity')
        city = request.form.get('city')

        if not student_id or not activity or not city:
            flash("Please provide all fields.", "warning")
            return redirect(url_for('log_participation'))

        weather_data = get_weather(city)

        # Normalize the weather condition before saving
        raw_condition = weather_data.get('condition', 'Unknown')
        normalized_condition = WEATHER_LABEL_MAP.get(raw_condition, 'Cloudy')

        log = ParticipationLog(
            student_id=student_id,
            activity=activity,
            weather_condition=normalized_condition
        )

        db.session.add(log)
        db.session.commit()

        flash(f"Participation logged! Weather: {normalized_condition}", "success")
        return redirect('/')

    return render_template("log_participation.html", students=students)

# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)