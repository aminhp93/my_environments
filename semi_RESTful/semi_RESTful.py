from flask import Flask, render_template, request, redirect, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'amin')
app.secret_key = "fasdk jf"

@app.route("/users/new")
def index():
	return render_template('new.html')

@app.route("/create", methods=['POST'])
def create():
	name = request.form['name']
	email = request.form['email']

	query = "INSERT INTO users(fullname, email, created_at) VALUES (:fullname, :email, NOW())"
	data = {'fullname': name, 'email': email}
	insert = mysql.query_db(query, data)

	return redirect('/users')

@app.route('/users')
def users():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)

	return render_template('index.html', users = users)

@app.route('/users/<user_id>')
def show(user_id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {'id': user_id}
	user = mysql.query_db(query, data)

	return render_template('show.html', user = user)

@app.route('/users/<user_id>/edit')
def edit(user_id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {'id': user_id}
	user = mysql.query_db(query, data)

	return render_template('edit.html', user = user)

@app.route('/users/<user_id>/update', methods=['POST'])
def update(user_id):
	query = "UPDATE users SET fullname = :fullname, email = :email, created_at = NOW() WHERE id = :id"
	data = {'fullname': request.form['fullname'], 'email': request.form['email'], 'id': user_id}
	mysql.query_db(query, data)

	return redirect('/users/' + user_id)

@app.route('/users/<user_id>/delete')
def delete(user_id):
	query = 'DELETE FROM users WHERE id = :id'
	data = {'id': user_id}
	insert = mysql.query_db(query, data)

	return redirect('/users')

app.run(debug=True)