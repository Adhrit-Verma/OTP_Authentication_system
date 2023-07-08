from flask import Flask, render_template, request, redirect, url_for
from modules import db_creator
from modules.db_creator import check
import mysql.connector as connector
from twilio.rest import Client
import random
import cred

class server_start():
    def __init__(self):
        con = connector.connect(host='localhost', port='3306', user='root', password='root')
        try:
            if con.is_connected():
                target_db = "users"
                db_checker = db_creator.db_check(target_db)
                if db_checker.check_exists():
                    print("Database exists")
                else:
                    database = db_creator.creator()
        except Exception as e:
            print(e)

s = server_start()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getotp', methods=['POST'])
def getotp():
    number = request.form['number']
    password = request.form['password']

    # Verify user credentials from the database
    user_checker = check(number, password)
    if user_checker.get_result():
        # User credentials are valid, proceed with OTP generation and login
        val = getOTPApi(number)
        (stat, otp) = val
        otp_validation(number, otp)  # Pass the number and OTP to the validation route
        if stat:
            return render_template('enterOtp.html')
    else:
        # User credentials are invalid, display an error message
        return render_template('login.html', message='Invalid username or password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']

        try:
            # Check if the user already exists
            user_checker = check(phone, password)
            if user_checker.get_result():
                return "User already exists with the provided phone number."

            # Insert the new user into the database
            con = connector.connect(host='localhost', port='3306', user='root', password='root', database='users')
            cur = con.cursor()
            query = "INSERT INTO Users (user_name, password, phone) VALUES (%s, %s, %s)"
            values = (username, password, phone)
            cur.execute(query, values)
            con.commit()
            con.close()

            return redirect(url_for('login'))
        except connector.Error as e:
            return f"An error occurred while registering the user: {e}"

    # Fetch the existing users from the database
    con = connector.connect(host='localhost', port='3306', user='root', password='root', database='users')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    users = cur.fetchall()
    con.close()
    return render_template('register.html', users=users)

@app.route('/validateOTP', methods=['POST'])
def otp_validation():
    user_otp = request.form['otp']
    number = request.form['number']
    if user_otp == request.form['otp']:
        return render_template('home.html', message='Login Successful!')
    else:
        return render_template('enterOtp.html', number=number, otp=user_otp, message='Wrong OTP')

def getOTPApi(number):
    account_sid = 'AC651d041e7edef1fd82d5927925640afb'
    auth_token = cred.auth()
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    body = "Your OTP is " + str(otp)
    message = client.messages.create(from_='+16183504860', body=body, to=number)
    if message.sid:
        return True, otp
    else:
        return False

def generateOTP():
    return random.randrange(10000, 99999)

if __name__ == '__main__':
    app.run()
