import random
import datetime
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'Codingdojo43'

def activities(coin, earn, farm):
	time = datetime.datetime.now()
	if earn == 'earn':
		session['activities'].append(['green','Earned ' + str(coin) + 'golds from the ' + str(farm) + str(time)])
	elif earn == 'lost':
		session['activities'].append(['red','Entered a casino and lost ' + str(coin) + 'Ouch...' + str(time)])
	return session['activities']

@app.route('/')
def index():
	if session.get('result') == None:
		session['result'] = 0
	if session.get('activities') == None:
		session['activities'] = []

	return render_template('index.html', activities = session['activities'])

@app.route('/process_money', methods=['POST'])
def process_money():
	if request.form['hidden'] == 'farm':
		coin = random.randint(10, 21)
		session['result'] += coin
		activities(coin, 'earn', 'farm')
	elif request.form['hidden'] == 'cave':
		coin = random.randint(5, 11)
		session['result'] += coin
		activities(coin, 'earn', 'cave')
	elif request.form['hidden'] == 'house':
		coin = random.randint(2,6)
		session['result'] += coin
		activities(coin, 'earn', 'house')
	elif request.form['hidden'] == 'casino':
		coin = random.randint(0, 50)
		win = random.randint(0,2)
		if win == 1:
			session['result'] += coin
			activities(coin, 'earn', 'casino')
		elif win == 0:
			session['result'] -= coin
			activities(coin, 'lost', 'casino')

	return redirect('/')

app.run(debug=True)

