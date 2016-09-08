import random
from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)
app.secret_key = 'ninja gold'

def init():
	session['your_gold'] = 0

@app.route('/')
def index():
	init()
	print session.items()
	return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():
	session['farm'] = random.randint(1,6)
	# session['your_gold'] += 

	return redirect('/')

app.run(debug=True)

