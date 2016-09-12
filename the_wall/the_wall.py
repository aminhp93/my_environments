from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
app.secret_key = "the wall"
mysql = MySQLConnector(app, 'the_wall')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    if not 'logged_in_id' in session:
        session['logged_in_id'] = ""
    if not 'id' in session:
        session['id'] = ""
    if not 'user_id' in session:
        session['user_id'] = ""
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest();
    password_confirmation = md5.new(request.form['password_confirmation']).hexdigest();

    # check validation

    error = 0

    if len(first_name) < 1:
        flash('First name can not be blank', 'firstNameError')
        error += 1

    if len(last_name) < 1:
        flash('Last name can not be blank', 'lastNameError')
        error += 1
    # elif last_name.isalpha() == False:
    #     flash('Last name can only contain letter', 'lastNameError')
    #     error += 1

    if not EMAIL_REGEX.match(email):
        flash('Invalid email', 'emailError')
        error += 1
    
    if len(request.form['password']) < 8:
        flash('Password has at least 8 characters', 'passwordError')
        error += 1

    if password != password_confirmation:
        flash('Password and confirmation is not match', 'passwordError')
        error += 1

    if error > 0:
        return redirect('/')

    query = 'INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())'
    data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password}
    session['id'] = mysql.query_db(query, data)
    return redirect('/users')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email_login']
    password = md5.new(request.form['password_login']).hexdigest();
    
    # check id in session
    if 'id' in session and session['id'] != "":
        pass
   
    # check id in database
    query = "SELECT * FROM users WHERE email = :email AND password = :password LIMIT 1"
    data = {'email': email, 'password': password}
    user = mysql.query_db(query, data)

    if user == []:
        flash('Email and password are not matched 2', 'emailLoginError')
        return redirect('/')

    session['logged_in_id'] = user[0]['id']

    return redirect('/users')

@app.route('/users')
def users():
    query = "SELECT * FROM users WHERE id = :id"

    # check id in session
    if 'id' in session and session['id'] != "":
        data = {'id': session['id']}
    else:
        data = {'id': session['logged_in_id']}

    # print session['logged_in_id']
    user = mysql.query_db(query, data)
    user[0]['id'] = int(user[0]['id'])
    session['user_id'] = user[0]['id']

    query = "SELECT messages.id, messages.created_at, messages.message, users.first_name, users.last_name FROM messages LEFT JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC"
    messages = mysql.query_db(query)

    query = "SELECT comments.message_id, users.first_name, users.last_name, comments.comment, comments.created_at FROM comments LEFT JOIN users ON comments.user_id = users.id"

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
    session.pop('id', None)
    session.pop('logged_in_id', None)
    session.pop('user_id', None)
    return redirect("/")

app.run(debug=True)