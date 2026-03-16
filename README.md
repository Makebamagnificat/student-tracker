# Student Class Participation Tracker + Weather Influence

A Flask web application used by lecturers and student leaders to track 
classroom participation and analyze how weather affects student engagement.

## Features
- Log participation (answering questions, asking questions, activity involvement)
- Fetch real-time weather for school location using OpenWeatherMap API
- Save participation logs in MySQL database
- Filter participation by date, weather condition, or student
- Dashboard showing weather influence on class activity count

## Tech Stack
- Python / Flask
- MySQL + SQLAlchemy
- Flask-Login / Flask-Bcrypt
- Chart.js
- OpenWeatherMap API

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Create MySQL database: `CREATE DATABASE student_tracker;`
3. Update `app.py` with your MySQL credentials
4. Run: `python app.py`
5. Visit: `http://127.0.0.1:5000`