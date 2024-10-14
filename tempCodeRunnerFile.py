from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Connect to MySQL database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",  # Change this to your MySQL password
        database="ngo"  # Updated database name
    )
    print(f"Database connection successful. Connected to database: {mydb.database}")
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Password pattern for validation
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

@app.route('/')
def landing():
    return render_template('landing.html')  # The main landing page

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user from MySQL database
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM client WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):  # Assuming the hashed password is in the 4th column
            print("User logged in successfully!")
            return redirect(url_for('index'))  # Redirect to index page upon successful login
        else:
            flash("Invalid username or password")  # Flash message for invalid login
            print("Login failed!")

    return render_template('landing.html')  # Always return the landing page

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Get the selected role from the form

        # Validate the password using regex
        if not re.match(PASSWORD_PATTERN, password):
            flash("Password must include at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.")
            return render_template('landing.html')  # Stay on the page with an error message

        # Check if the username or email already exists
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM client WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or email already exists.")
            return render_template('landing.html')  # Stay on the page with an error message

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # Insert the new user's information into the database
        try:
            print(f"Attempting to insert user: {username}, {email}, role: {role}")
            cursor.execute("INSERT INTO client (username, email, password, role) VALUES (%s, %s, %s, %s)", (username, email, hashed_password, role))
            mydb.commit()  # Commit the transaction
            print("Data inserted successfully!")  # Confirmation message
            flash("Registration successful! Please log in.")  # Show success message
            return render_template('landing.html')  # Stay on login page
        except mysql.connector.Error as err:
            mydb.rollback()  # Rollback if there's an error
            flash(f"Error: {str(err)}")  # Flash error message
            print(f"Error during insertion: {err}")  # More detailed logging
            return render_template('landing.html')

    return render_template('landing.html')  # Always return the landing page

# Index route (homepage after login)
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
