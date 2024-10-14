import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtCore import QDate
import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-645TUK7'
DATABASE_NAME = 'AccountingHuDb'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    uid=<hu>;
    password=<mariasamadproject>;
"""
connection = odbc.connect(connection_string)

print('Connected to the database')
print('Connection:', connection)

# get all data from user table
# cursor = connection.cursor()
# cursor.execute('SELECT * FROM [User]')
# for row in cursor.fetchall():
#     print(row)
# connection.close()


import datetime
# Returns the current local date


class Login(QtWidgets.QMainWindow):
    def __init__(self):
    # Call the inherited classes __init__ method
        super(Login, self).__init__()
        # Load the .ui file
        uic.loadUi('./UIs/UserLogin.ui', self)
        
        # Show the GUI
        self.show()

        # Connect the login button to a function
        self.pushButton.clicked.connect(self.login)
        # Connect the signup button to a function which changes window to signup window
        self.signupButton.clicked.connect(self.signup_window)

    def signup_window(self):
        self.signup = Signup()
        self.signup.show()
        self.close()

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if not username or not password:
            #alert
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Login Failed')
            message_box.setText('Username and Password are required')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        # get all data from user table
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Users] WHERE User_Name = '{username}' AND Password = '{password}'")
        user = cursor.fetchone()
        if user:
            if user[4] == True:
                #alert 
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Login Successful')
                message_box.setText(f"Welcome {user[1]}, UserID = {user[0]}")
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
            else:
                # alert the user using message box that user is not approved
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Login Failed')
                message_box.setText('User is not approved')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
        else:
            # alert the user using message box that the login failed
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Login Failed')
            message_box.setText('Invalid Username or Password')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()

class Signup(QtWidgets.QMainWindow):
    def __init__(self):
    # Call the inherited classes __init__ method
        super(Signup, self).__init__()
        # Load the .ui file
        uic.loadUi('./UIs/UserRegisteration.ui', self)
        
        # Show the GUI
        self.show()

        # Connect the button to a function
        self.pushButton.clicked.connect(self.signup)
        # Connect the login button to a function which changes window to signup window
        self.loginButton.clicked.connect(self.login_window)

    def login_window(self):
        self.login = Login()
        self.login.show()
        self.close()

    def signup(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirm_password = self.confirmPasswordLineEdit.text()

        #check if user already exists
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Users] WHERE User_Name = '{username}'")
        user = cursor.fetchone()
        if user:
            #alert
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Signup Failed')
            message_box.setText('Username already exists')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            if not username or not password or not confirm_password:
                print('Username, Password and Confirm Password are required')
                return
            if password != confirm_password:
                print('Password and Confirm Password must match')
                return
            date = datetime.datetime.now().date()
            # make a user object but keep approved = false
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO [Users] (User_Name, Password, Creation_Date, Approved) VALUES ('{username}', '{password}', '{date}', '0')")
            connection.commit()
            #alert
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Signup Successful')
            message_box.setText('User Registered Successfully')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()


    
        


# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)
window = Login() # Create an instance of our class
app.exec() # Start the application