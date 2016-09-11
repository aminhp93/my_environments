from flask import Flask, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
app.secret_key = "Coding dodofasfa "
mysql = MySQLConnector(app, 'the_wall')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():

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

    user = mysql.query_db(query, data)
    session['current_id'] = user[0]['id']

    return render_template('user.html', user = user, messages = session['all_messages'])

@app.route('/messages', methods=['POST'])
def messages():
    message = request.form['message']

    query = "INSERT INTO messages(message, user_id, created_at, updated_at) VALUES (:message, :user_id, NOW(), NOW())"
    data = {'message': message, 'user_id': session['current_id']}
    display = mysql.query_db(query, data)

    query = "SELECT * FROM messages"
    session['all_messages'] = mysql.query_db(query)

    query = "INSERT INTO comments(comment, user_id, message_id, created_at, updated_at) VALUES (:comment, :user_id, :message_id, NOW(), NOW())"
    data = {'comment': comment, 'user_id': session['current_id'], 'message_id': current_message}

    query = "SELECT * FROM comments"
    comment = mysql.query_db(query)


    return redirect('/users')

@app.route('/comments', methods=['POST'])
def comments():
    return redirect('/users')















app.run(debug=True)