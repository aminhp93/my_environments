from flask import Flask, render_template, redirect, request, session, flash
import re
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
  return render_template('index.html')
@app.route('/process', methods=['Post'])
def process():
  #do some validations here!
  if len(request.form['email']) < 1:
  	flash("Email cannot be empty")
  elif not EMAIL_REGEX.match(request.form['email']):
  	flash("invalid email address")
  else:
  	flash("Success")

  return redirect('/')


app.run(debug=True)