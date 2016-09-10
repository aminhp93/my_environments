from flask import Flask, render_template, request, redirect, flash, session
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "Coding dojo1"
mysql = MySQLConnector(app, 'amin')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
	query = "SELECT * FROM friends"
	all_friends = mysql.query_db(query)
	return render_template('index.html', friends = all_friends)

@app.route('/friends', methods=['POST'])
def create():
	name = request.form['name']
	if name == "":
		flash("Name can not be empty")
		return redirect('/')
	else:
		query = "INSERT INTO friends(name, created_at, updated_at) VALUES (:name, NOW(), NOW())"
		data = {'name': name}
		insert_query = mysql.query_db(query, data)
		# flash("You collected " + name + " .Congratulation!")
		return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	query = "SELECT * FROM friends WHERE id = :id"
	data = {'id': id}
	all_friends = mysql.query_db(query,data)
	return render_template('edit.html', friends=all_friends)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	query = "UPDATE friends SET name = :name WHERE id = :id"
	data = {'name': request.form['name'], 'id': id}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/delete')
def delete(id):
	query = "SELECT * FROM friends"
	display_query = mysql.query_db(query)
	name = display_query[int(id)]['name']
	flash('Deleted ' + name + ' successfully!')
	query1 = "DELETE FROM friends WHERE id = :id"
	data = {'id': id}
	mysql.query_db(query1, data)
	return redirect('/')

app.run(debug=True)