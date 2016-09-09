from flask import Flask, render_template, request, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'Codsfs'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	name = request.form['name']
	location = request.form['location']
	language = request.form['language']
	comment = request.form['comment']

	if name == "" or comment == "" :
		flash('Name or comment can not be blank')
		return redirect('/')

	if (comment) > 120:
		flash("Comment cannot be longer than 120 chars")
		return redirect('/')

	# data = {'name': name, 'locaiton': locaiton, 'language': language, 'comment': comment}
	return render_template('result.html', name = name, location = location, language = language, comment = comment)

app.run(debug=True)