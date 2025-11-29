from flask import Flask, render_template, redirect, request, url_for, jsonify, session
import sqlite3, os, uuid, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from shortlink_db import ShortLinkDB
from datetime import datetime

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'image', 'template'))
app = Flask(__name__, template_folder=template_dir)
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'static', 'image', 'template')
static_dir = os.path.join(base_dir, 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.secret_key = 'your-secret-key-change-this'
 
db = ShortLinkDB("shortlinks.db")


DB_PATH = "courses.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS courses
                 (id INTEGER PRIMARY KEY, title TEXT, price TEXT, duration TEXT, days TEXT, time TEXT, created_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS institute_info
                 (id INTEGER PRIMARY KEY, name TEXT, intake TEXT, image_path TEXT, requirements TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, message TEXT, created_at TIMESTAMP)''')
    conn.commit()
    
    c.execute('SELECT COUNT(*) FROM courses')
    if c.fetchone()[0] == 0:
        default_courses = [
            ("IT Fundamental / Office Basic", "$50 USD", "10 weeks", "Mondays & Wednesday", "2:30 PM – 4:00 PM"),
            ("Web Development (HTML, CSS, JavaScript)", "$60 USD", "10 weeks", "Mondays & Wednesday", "4:00 PM – 5:30 PM"),
            ("Business Accounts (QuickBook)", "$60 USD", "6 weeks", "Tuesday & Thursday", "2:30 PM – 4:00 PM"),
            ("Computer Networking & Protocol", "$50 USD", "8 weeks", "Tuesday & Thursday", "4:30 PM – 5:00 PM"),
            ("Digital Marketing & Brand Management", "$60 USD", "8 weeks", "Friday", "2:30 PM – 4:00 PM"),
            ("Graphic Design", "$50 USD", "8 weeks", "Friday", "4:00 PM – 5:30 PM")
        ]
        for course in default_courses:
            c.execute('INSERT INTO courses (title, price, duration, days, time, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                     (*course, datetime.now()))
        conn.commit()
    
    c.execute('SELECT COUNT(*) FROM institute_info')
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO institute_info (name, intake, image_path, requirements) 
                      VALUES (?, ?, ?, ?)''',
                  ("SoftNet Africa", "2025 INTAKE", "/static/image/logo.png", 
                   "Registration: $5 USD|ID Card: (confirm amount)|T-Shirt: $5 USD"))
        conn.commit()
    
    conn.close()
   
def get_institute():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, intake, image_path, requirements FROM institute_info LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "name": row[0],
            "intake": row[1],
            "image_path": row[2],
            "general_requirements": row[3].split('|')
        }
    return None

def get_courses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title, price, duration, days, time FROM courses ORDER BY id')
    courses = [{"id": row[0], "title": row[1], "price": row[2], "duration": row[3], "days": row[4], "time": row[5]} for row in c.fetchall()]
    conn.close()
    return courses

init_db()

@app.route("/")
def index():
    institute = get_institute()
    courses = get_courses()
    
    base_url = request.url_root.rstrip("/")
    full_link = f"{base_url}/"
    short_link = db.get_or_create_short_link(full_link)

    share_text = f"{institute['name']} {institute['intake']} → {short_link}"
    links = {
        "full": short_link,
        "twitter": f"https://twitter.com/intent/tweet?text={share_text}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={short_link}",
        "whatsapp": f"https://api.whatsapp.com/send?text={share_text}"
    }

    return render_template("index.html", institute=institute, courses=courses, share_links=links)

@app.route("/contact", methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()
    
    if not all([name, email, phone, message]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, email, phone, message, created_at) VALUES (?, ?, ?, ?, ?)',
             (name, email, phone, message, datetime.now()))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True}), 200

@app.route("/admin")
def admin():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    institute = get_institute()
    courses = get_courses()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, email, phone, message, created_at FROM contacts ORDER BY created_at DESC')
    contacts = [{"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "message": row[4], "created_at": row[5]} for row in c.fetchall()]
    conn.close()
    
    return render_template("admin.html", institute=institute, courses=courses, contacts=contacts)

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'adminsoftnet@#':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        return render_template("admin_login.html", error="Invalid password"), 401
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route("/api/course", methods=['POST'])
def add_course():
    if 'admin_logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO courses (title, price, duration, days, time, created_at) VALUES (?, ?, ?, ?, ?, ?)',
             (data['title'], data['price'], data['duration'], data['days'], data['time'], datetime.now()))
    course_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"id": course_id}), 201

@app.route("/api/course/<int:course_id>", methods=['PUT', 'DELETE'])
def manage_course(course_id):
    if 'admin_logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        c.execute('UPDATE courses SET title=?, price=?, duration=?, days=?, time=? WHERE id=?',
                 (data['title'], data['price'], data['duration'], data['days'], data['time'], course_id))
    elif request.method == 'DELETE':
        c.execute('DELETE FROM courses WHERE id=?', (course_id,))
    
    conn.commit()
    conn.close()
    return jsonify({"success": True}), 200

@app.route("/r/<code>")
def redirect_short(code):
    url = db.get_url(code)
    return redirect(url) if url else ("Link expired or not found", 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
