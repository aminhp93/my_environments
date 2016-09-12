from flask import Flask, render_template, request, redirect, flash, session
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "COfsdfsdfd"
mysql = MySQLConnector(app, 'amin')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
	session['first_name'] = ""
	session['last_name'] = ""
	session['email'] = ""
	session['password'] = ""
	session['confirm_password'] = ""
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

	session['first_name'] = request.form['first_name']
	session['last_name'] = request.form['last_name']
	session['email'] = request.form['email']
	session['password'] = request.form['password']
	session['confirm_password'] = request.form['password_confirmation']

	error = 0

	if len(session['first_name']) < 2 or session['first_name'].isalpha() == False:
		flash('First Name cannot be blank, letter only', 'firstNameError') 
		error += 1

	if len(session['last_name']) < 2 or session['last_name'].isalpha() == False:
		flash('Last Name cannot be blank, letter only', 'lastNameError') 
		error += 1

	if not EMAIL_REGEX.match(session['email']):
		flash('Invalid Email', 'emailError')
		error += 1

	if len(session['password']) < 8:
		flash('Password At least 8 character', 'passwordError')
		error += 1
	if session['password'] != session['confirm_password']:
		flash('Password is not match', 'confirmationPasswordError')
		error += 1

	if error > 0:
		return redirect('/')

	query = "INSERT INTO log_in(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
	data = {'first_name': session['first_name'], 'last_name': session['last_name'], 'email': session['email'], 'password': session['password']}
	session['id'] = mysql.query_db(query, data)
	return redirect('success')

@app.route('/success')
def success():
	query = "SELECT * FROM log_in WHERE id = :id"

	if 'id' in session:
		data = {'id': session['id']}
	else:
		data = {'id': session['logged_in_id']}
	
	user = mysql.query_db(query, data)
	user[0]['id'] = int(user[0]['id'])

	return render_template('success.html', user = user)

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']

	if 'id' in session:
		query = "SELECT * FROM log_in WHERE id = :id"
		data = {'id': session['id']}
		user = mysql.query_db(query, data)
		if user[0]['email'] != email or user[0]['password'] != password:
			flash('Email and Password are not matched')
			return redirect('/')

	query = "SELECT * FROM log_in WHERE email = :email AND password = :password LIMIT 1"
	data = {'email': email, 'password': password}
	user = mysql.query_db(query, data)

	if len(user) == 0:
		flash('Wrong password or email when logging in')
		redirect('/')

	session['logged_in_id'] = user[0]['id']

	return redirect('success')
app.run(debug=True)