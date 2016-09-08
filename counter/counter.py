from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'ThisisSecret'

def count():
	try:
		session['times'] += 1
	except KeyError:
		session['times'] = 0

@app.route('/')
def index():
	count()
	return render_template('index.html')

@app.route('/page2')
def page2():
	session['times'] += 1
	return redirect('/')

@app.route('/reset')
def reset():
	session['times'] = -1
	return redirect('/')

app.run(debug=True)
