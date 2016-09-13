from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
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
    password = bcrypt.generate_password_hash(request.form['password'])

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

    if request.form['password'] != request.form['password_confirmation']:
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
    password = request.form['password_login']
    
    # check id in session
    if 'id' in session and session['id'] != "":
        pass
   
    # check id in database
    query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    data = {'email': email}
    user = mysql.query_db(query, data)

    if bcrypt.check_password_hash(user[0]['password'], password):
        session['logged_in_id'] = user[0]['id']
        return redirect('/users')
    else:
        flash('Email and password are not matched 2', 'emailLoginError')
        return redirect('/')

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

    query = "SELECT messages.user_id, messages.id, messages.created_at, messages.message, users.first_name, users.last_name FROM messages LEFT JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC"
    messages = mysql.query_db(query)

    query = "SELECT comments.user_id, comments.id, comments.message_id, users.first_name, users.last_name, comments.comment, comments.created_at FROM comments LEFT JOIN users ON comments.user_id = users.id"

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

@app.route('/messages/<message_id>/edit')
def edit_message(message_id):
    query = 'SELECT * FROM messages WHERE id = :id LIMIT 1'
    data = {'id': message_id}
    message = mysql.query_db(query, data)

    return render_template('edit_message.html', message = message)

@app.route('/messages/<message_id>', methods=['POST'])
def update_message(message_id):
    query = 'UPDATE messages SET message = :message WHERE id = :id'
    data = {'message': request.form['update_message'], 'id': message_id}
    insert = mysql.query_db(query, data)
    
    return redirect('/users')

@app.route('/messages/<message_id>/delete', methods=['POST'])
def delete_message(message_id):
    query = "DELETE FROM messages WHERE id = :id"
    data = {'id': message_id}
    insert = mysql.query_db(query, data)

    query = "DELETE FROM comments WHERE message_id = :message_id"
    data = {'message_id': message_id}
    insert = mysql.query_db(query, data)

    return redirect('/users')

@app.route('/comments/<comment_id>/edit')
def edit_comment(comment_id):
    query = 'SELECT * FROM comments WHERE id = :id LIMIT 1'
    data = {'id': comment_id}
    comment = mysql.query_db(query, data)
    
    return render_template('edit_comment.html', comment = comment)

@app.route('/comments/<comment_id>', methods=['POST'])
def update_comment(comment_id):
    query = 'UPDATE comments SET comment = :comment WHERE id = :id'
    data = {'comment': request.form['update_comment'], 'id': comment_id}
    insert = mysql.query_db(query, data)
    
    return redirect('/users')

@app.route('/comments/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    query = "DELETE FROM comments WHERE id = :id"
    data = {'id': comment_id}
    insert = mysql.query_db(query, data)

    return redirect('/users')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id', None)
    session.pop('logged_in_id', None)
    session.pop('user_id', None)
    
    return redirect("/")

app.run(debug=True)