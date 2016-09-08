import random 
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'Codingdojo'

def randomNUmber():
	session['secret'] = random.randint(1, 101)

@app.route('/')
def index():
	print session.items()
	return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    session['guess'] = int(request.form['guess'])
    return redirect('/')

@app.route('/reset')
def reset():
    session.pop('number')
    return redirect('/')


app.run(debug=True)