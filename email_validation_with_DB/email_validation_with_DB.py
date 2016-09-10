from flask import Flask, render_template, request, redirect, flash, session
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "Coding dojo1"
mysql = MySQLConnector(app, 'amin')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	email = request.form['email']
	if not EMAIL_REGEX.match(email):
		flash('Invalid email')
		return redirect('/')
	else:
		query1 = "INSERT INTO table_email(email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		data = {
				 'email': request.form['email']
			   }
		insert_query1 = mysql.query_db(query1, data)
		
		flash('The email addess you entered' + email + 'is a VALID email address! Thank you!')
		return redirect('/success')

@app.route('/success')
def success():
	query2 = "SELECT * FROM table_email"
	display_query2 = mysql.query_db(query2)

	return render_template('success.html', emails = display_query2)	

@app.route('/delete', methods=['POST'])
def delete():
	query2 = "SELECT * FROM table_email"
	display_query2 = mysql.query_db(query2)
	email = display_query2[-1]['email']
	query1 = "DELETE FROM table_email ORDER BY id DESC LIMIT 1"
	mysql.query_db(query1)
	flash('Deleted ' + email + ' successfully!')
	return redirect('/success')

app.run(debug=True)
