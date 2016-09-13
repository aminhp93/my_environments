from flask import Flask, render_template, request, redirect, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'amin')

@app.route('/')
def index():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)
	return render_template('index.html', users = users)

@app.route("/users/new", methods=['POST'])
def create():
	name = request.form['name']
	email = request.form['email']

	query = "INSERT INTO users(name, email, created_at) VALUES (:name, :email, NOW())"
	data = {'name': name, 'email': email}
	insert = mysql.query_db(query, data)

	return render_template('new.html')

app.run(debug=True)