from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
import base64
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from random import randint
from connect import *

@login_manager.user_loader
@app.route('/')
def index():
    return render_template('index.html', method='utf-8')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    cur = conn.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    captcha_response = request.form['g-recaptcha-response']
    if str(captcha_response)=='':
        return redirect('/login')
    cur.execute(f"SELECT id, name, email, password FROM users WHERE email='{email}';")
    val = cur.fetchone()
    print(val)
    check_avalibility = val
    print(check_avalibility)
    if check_avalibility == False:
        flash('Email введён неверно')
        return redirect(url_for('login'))
    user = {}
    user['id'] = check_avalibility[0]
    user['name'] = check_avalibility[1]
    user['email'] = check_avalibility[2]
    user['password'] = check_avalibility[3]
    if check_password_hash(user['password'], password)==False:
        flash('Пароль введён неверно')
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    cur = conn.cursor()
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')
    captcha_response = request.form['g-recaptcha-response']
    if str(captcha_response)=='':
        return redirect('/signup')
    cur.execute(f"SELECT * FROM users WHERE email='{email}';")
    mail = cur.fetchone()
    cur.execute(f"SELECT * FROM users WHERE phone='{phone}';")
    num = cur.fetchone()
    cur.execute(f"SELECT * FROM users WHERE name='{name}';")
    login = cur.fetchone()

    if mail:
        flash('Email занят')
        return redirect(url_for('signup'))
    elif num:
        flash('Тел.номер занят')
        return redirect(url_for('signup'))
    elif login:
        flash('Login занят')
        return redirect(url_for('signup'))
    elif len(password) < 8:
        flash('Пароль меньше 8 символов')
        return redirect(url_for('signup'))

    cur.execute(f"INSERT INTO users (phone, name, email, password) VALUES('{phone}', '{name}', '{email}', '{generate_password_hash(password, method='sha256')}');")
    conn.commit()
    cur.close()

    return redirect(url_for('login'))

app.secret_key = 'some_secret_key'
if __name__ == "__main__":
    app.run(debug=True)