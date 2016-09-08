from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "This is secret1"

amin = 10
def init():
	session['amin'] = 4
	print session['amin']

@app.route('/')
def index():
	print amin
	print session['amin']
	return render_template('index.html')

@app.route('/users', methods=['POST'])
def users():
	session['name'] = request.form['name']
	session['email'] = request.form['email']
	return redirect('/show')

@app.route('/show')
def show():
	return render_template('users.html', name=session['name'], email=session['email'])

app.run(debug=True)
