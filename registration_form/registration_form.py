from flask import Flask, render_template, request, redirect, flash, session
import re
app = Flask(__name__)
app.secret_key = 'Codsfs'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['confirm_password']
	location = request.form['location']
	language = request.form['language']
	comment = request.form['comment']

	if first_name == "" or last_name == "" or comment == "" or email == "" or password == "":
		flash('Can not be blank')
		return redirect('/')
	elif bool(re.search(r'\d', first_name)) == True or bool(re.search(r'\d', last_name)) == True:
		flash('name can not contain number')
		return redirect('/')
	elif len(password) > 8:
		flash('password can not be more than 8 chars')
		return redirect('/')
 	elif not EMAIL_REGEX.match(request.form['email']):
  		flash("invalid email address")
  		return redirect('/')
  	elif password != confirm_password:
  		flash("Password and Password Confirmation should match")
  		return redirect('/')
	elif (comment) > 120:
		flash("Comment cannot be longer than 120 chars")
		return redirect('/')
	else:
		flash("Thanks for submitting your information")

	# data = {'name': name, 'locaiton': locaiton, 'language': language, 'comment': comment}
	return render_template('result.html', name = name, location = location, language = language, comment = comment)

app.run(debug=True)