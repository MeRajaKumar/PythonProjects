import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('school_attendance.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Classes (
                        class_id INTEGER PRIMARY KEY,
                        class_name TEXT,
                        teacher_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                        student_id INTEGER PRIMARY KEY,
                        name TEXT,
                        class_id INTEGER,
                        enrollment_date TEXT,
                        FOREIGN KEY (class_id) REFERENCES Classes(class_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                        subject_id INTEGER PRIMARY KEY,
                        subject_name TEXT,
                        class_id INTEGER,
                        FOREIGN KEY (class_id) REFERENCES Classes(class_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
                        attendance_id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        subject_id INTEGER,
                        attendance_date TEXT,
                        status TEXT,
                        FOREIGN KEY (student_id) REFERENCES Students(student_id),
                        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id))''')
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()
