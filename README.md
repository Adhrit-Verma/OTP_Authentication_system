
# Flask User Management System

This is a Flask-based user management system that allows users to register, log in, and perform various operations such as updating and deleting user records. It uses MySQL as the database and Twilio for sending OTP (One-Time Password) messages.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

2. Extract the `cred.rar` file:

   - The `cred.rar` file contains a Python file named `cred.py`, which is required for the application to work.
   - Extract the contents of the `cred.rar` file into the project directory.

3. Set up the virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Register a new user by filling out the registration form.
- Log in with the registered credentials.
- Perform various operations such as updating user details or deleting a user.
- Users can also request an OTP (One-Time Password) for verification.

## Credits

The application uses the following dependencies:

- Flask (2.0.1)
- mysql-connector-python (8.0.27)
- twilio (6.64.0)

Make sure to review the license information of each dependency.

## License

[MIT License](LICENSE)
```

Make sure to include the `cred.rar` file in your project repository or provide instructions on how to obtain it separately, as mentioned in the installation steps.