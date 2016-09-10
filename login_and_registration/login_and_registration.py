from flask import Flask, render_template, request, redirect, flash, session
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "COafsdfsdf"
mysql = MySQLConnector(app, 'amin')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['password_confirmation']

	if len(first_name) < 2 or first_name.isalpha() == False:
		flash('Name cannot be blank, letter only') 
		return redirect('/')
	elif len(last_name) < 2 or last_name.isalpha() == False:
		flash('Name cannot be blank, letter only') 
		return redirect('/')
	elif not EMAIL_REGEX.match(email):
		flash('Invalid Email')
		return redirect('/')
	elif len(password) < 8:
		flash('Password At least 8 character')
		return redirect('/')
	elif password != confirm_password:
		flash('Password is not match')
		return redirect("/")

	query = "INSERT INTO log_in(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
	data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password}
	session['id'] = mysql.query_db(query, data)
	return redirect('success')

@app.route('/success')
def success():
	query = "SELECT * FROM log_in WHERE id = :id"
	data = {'id': session['id']}
	user = mysql.query_db(query, data)

	return render_template('success.html', user = user)

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	query = "SELECT * FROM log_in WHERE id = :id"
	data = {'id': session['id']}
	user = mysql.query_db(query, data)

	if user[0]['email'] != email or user[0]['password'] != password:
		flash('Email and Password are not matched')
		return redirect('/')

	return redirect('success')
app.run(debug=True)