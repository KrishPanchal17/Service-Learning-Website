from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import re

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="W7301@jqir#",
    database="website"
)
if mydb.is_connected():
    print("Connected to MySQL database")
else:
    print("Failed to connect to MySQL database")
# Password pattern for validation
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message variable

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user against MySQL database
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):  # Assuming hashed password is stored in the fourth column
            print("User logged in successfully!")
            return redirect(url_for('index'))  # Redirect to index page on successful login
        else:
            error = "Invalid username or password"
            print("Invalid username or password!")

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate password
        if not re.match(PASSWORD_PATTERN, password):
            message = "Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character."
            return render_template('login.html', message=message)

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # Insert the new user's information into the database
        try:
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            mydb.commit()  # Commit the transaction
            message = "Registration successful! You can now log in."
            return render_template('login.html', message=message)  # Show a success message
        except mysql.connector.IntegrityError as err:
            if "Duplicate entry" in str(err):
                message = "Username or email already exists."
            else:
                message = f"Error: {str(err)}"
            return render_template('login.html', message=message)
        except mysql.connector.Error as err:
            message = f"Error: {str(err)}"
            print(message)  # Print error for debugging
            return render_template('login.html', message=message)

    return render_template('register.html', message=message)


# Add other routes, including the index route here

if __name__ == '__main__':
    app.run(debug=True)
