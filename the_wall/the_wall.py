from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
app.secret_key = "Con dodoff2a1"
mysql = MySQLConnector(app, 'the_wall')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    session['first_name'] = ""
    session['last_name'] = ""
    session['email'] = ""
    session['password'] = ""
    session['logged_in_id'] = ""
    session['id'] = ""
    session['user_id'] = ""
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']

    # validation

    query = 'INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())'
    data = {'first_name': session['first_name'], 'last_name': session['last_name'], 'email': session['email'], 'password': session['password']}
    session['id'] = mysql.query_db(query, data)
    return redirect('/users')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email_login']
    password = request.form['password_login']
    
    # check id in session
    if 'id' in session:
        query = "SELECT * FROM users WHERE id = :id"
        data = {'id': session['id']}
        user = mysql.query_db(query, data)
        if user[0]['email'] != email or user[0]['password'] != password:
            flash('Email and password are not matched')
            return redirect('/')

    # check id in database
    query = "SELECT * FROM users WHERE email = :email AND password = :password LIMIT 1"
    data = {'email': email, 'password': password}
    user = mysql.query_db(query, data)

    if len(user) == 0:
        flash('Wrong password or email when logging in')
        redirect('/')

    session['logged_in_id'] = user[0]['id']

    return redirect('/users')

@app.route('/users')
def users():
    query = "SELECT * FROM users WHERE id = :id"

    # check id in session
    if 'id' in session:
        data = {'id': session['id']}
    else:
        data = {'id': session['logged_in_id']}

    # print session['logged_in_id']
    user = mysql.query_db(query, data)
    user[0]['id'] = int(user[0]['id'])
    session['user_id'] = user[0]['id']

    query = "SELECT messages.id, messages.message, users.first_name, users.last_name FROM messages LEFT JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC"
    messages = mysql.query_db(query)

    query = "SELECT * FROM comments"

    comments = mysql.query_db(query)

    return render_template('user.html', user = user, messages = messages, comments = comments)

@app.route('/messages', methods=['POST'])
def messages():
    message = request.form['message']

    query = "INSERT INTO messages(message, user_id, created_at, updated_at) VALUES (:message, :user_id, NOW(), NOW())"
    data = {'message': message, 'user_id': session['user_id']}
    insert = mysql.query_db(query, data)

    return redirect('/users')

@app.route('/messages/<message_id>/comments', methods=['POST'])
def comments(message_id):
    comment = request.form['comment']

    query = "INSERT INTO comments(comment, user_id, message_id, created_at, updated_at) VALUES (:comment, :user_id, :message_id, NOW(), NOW())"
    data = {'comment': comment, 'user_id': session['user_id'], 'message_id': message_id}
    insert = mysql.query_db(query, data)

    return redirect('/users')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect("/")


app.run(debug=True)