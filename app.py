from flask import Flask, render_template, request,url_for,redirect
import firebase_admin
from modules import db_creator
from firebase_admin import credentials
from firebase_admin import auth
import mysql.connector

# Initialize Flask app
db = db_creator.creator()
app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate('service_firebase.json')
firebase_admin.initialize_app(cred)

# Initialize MySQL connection
mysql_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='users'
)

# Firebase phone number verification
def verify_phone_number(phone_number):
    try:
        user = auth.get_user_by_phone_number(phone_number)
        return user
    except auth.AuthError as e:
        return None

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form submission
        username = request.form.get('username')
        password = request.form.get('phone')
        check=db_creator.check(phone=)

        # Add your login logic here
        # Validate the username and password
        # Perform authentication

        # Redirect to a home page or dashboard upon successful login
        return redirect('/home')

    # Render the login page for GET requests
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    country_code = request.form['country_code']
    username = request.form['username']
    password = request.form['password']
    phone_number = request.form['phone_number']
    full_phone_number = country_code + phone_number
    
    # Store user information in MySQL database
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO users (user_name, password, phone) VALUES (%s, %s, %s)"
    values = (username, password, full_phone_number)
    cursor.execute(insert_query, values)
    mysql_connection.commit()
    cursor.close()

    # Create user in Firebase Authentication
    try:
        user = auth.create_user(phone_number=full_phone_number)
        return redirect(url_for('index', registrationSuccess='true'))
    except auth.AuthError as e:
        return 'Registration failed'
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
