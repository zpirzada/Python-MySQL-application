import mysql.connector
import boto3
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your own secret key

# Modify the following variables with your MySQL database credentials
ssm = boto3.client('ssm', region_name='us-east-1')
parameter_name = "mysql_psw" 
response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
mysql_password = response['Parameter']['Value']

# Connect to MySQL
db_connection = mysql.connector.connect(
    host="database-1.cnqaegruhvch.us-east-1.rds.amazonaws.com",
    user="admin",
    password=mysql_password,
    database="test"
)
db_cursor = db_connection.cursor()

# Create the 'users' table if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
"""
db_cursor.execute(create_table_query)

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert the user into the MySQL database
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        db_cursor.execute(insert_query, (username, password))
        db_connection.commit()

        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the MySQL database
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        db_cursor.execute(select_query, (username, password))
        user = db_cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Assuming 'id' is the first column in the 'users' table
            return redirect(url_for('dashboard'))

    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect(url_for('signin'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        # Fetch the username from the database based on user_id
        select_username_query = "SELECT username FROM users WHERE id = %s"
        db_cursor.execute(select_username_query, (user_id,))
        username = db_cursor.fetchone()[0]  # Fetch the first column (username)
        
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
