import md5
import os, binascii
password = 'password'
encrypted_password = md5.new(password).hexdigest()
print encrypted_password

# @app.route('/users/create', methods=['POST'])
# def create_user():
# 	username = request.form['username']
# 	email = request.form['email']
# 	password = md5.new(request.form['password']).hexdigest();
# 	insert_query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (:username, :email, :password, NOW(), NOW())"
# 	query_data = {'username': username, 'email': email, 'password': password}
# 	mysql.query_db(insert_query, query_data)

# 	user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"
# 	query_data = {'email': email, 'password': password}

salt = binascii.b2a_hex(os.urandom(15))
print os.urandom(15)
print salt
encrypted_password = md5.new(password + salt).hexdigest()
print encrypted_password