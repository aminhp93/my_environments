from flask import Flask, request, render_template
from mysqlconnection import MySQLConnector

from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'mydb')

pw_hash = bcrypt.generate_password_hash('hunter')
print pw_hash

app.run(debug=True)