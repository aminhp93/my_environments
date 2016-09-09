from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/users/<username>')
def show(username):
	return render_template('user.html', username = username)

app.run(debug=True)
