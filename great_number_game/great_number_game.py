
import random 
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'Codingdojo1'

@app.route('/')
def index():
	if not 'secret' in session:
		session['secret'] = random.randint(1, 101)
	print session.items()
	return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    session['guess'] = int(request.form['guess'])

    if session['guess'] < session['secret']:
    	session['result'] = 'Too low'
    	session['class'] = 'other'
    elif session['guess'] > session['secret']:
    	session['result'] = 'Too high'
    	session['class'] = 'other'
    else:
 		session['result'] = 'you are the winner. here is your number:' + str(session['secret'])
 		session['class'] = 'right'

    return redirect('/')

@app.route('/reset')
def reset():
    session.pop('secret', None)
    return redirect('/')

app.run(debug=True)
