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
# print('Connection:', connection)

# get all data from user table
cursor = connection.cursor()
cursor.execute('SELECT * FROM [Users]')
for row in cursor.fetchall():
    print(row)
# connection.close()


import datetime
# Returns the current local date

#variable so that when back button is pressed makes sure that the previous page is loaded

 


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
        previous_page = self
        self.close()


    def login(self):
        id = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if not id or not password:
            if type(id) != int:
                # alert the user using message box that the login failed
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Login Failed')
                message_box.setText('Invalid ID or Password')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
                return
            else:
                #alert
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Login Failed')
                message_box.setText('ID and Password are required')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
                return
        # get all data from user table
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Users] WHERE User_ID = '{id}' AND Password = '{password}'")
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
                if (user[0] == 1):
                    self.admin = AdminMain()
                    self.admin.show()
                    self.close()
                else:
                    self.ui = Ui()
                    self.ui.show()
                    self.close()
            else:
                # alert the user using message box that user is not approved
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Login Failed')
                message_box.setText('User ID is not approved')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
        else:
            # alert the user using message box that the login failed
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Login Failed')
            message_box.setText('Invalid ID or Password')
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


    
class Ui(QtWidgets.QMainWindow):
    previous_page = None

    def __init__(self,):
        super(Ui,self).__init__()
        uic.loadUi('./UIs/UserMain.ui',self)
        

  
        self.pushButton_2.clicked.connect(self.show_transaction)
        self.pushButton.clicked.connect(self.show_view_acc)
        self.pushButton_3.clicked.connect(self.show_report)
        self.logoutButton.clicked.connect(self.logout)


    
    def logout(self):
        self.view_pg = Login()
        self.view_pg.show()
        self.close()
    
    def show_transaction(self):
        previous_page = Ui()
        self.transac_pg = loadTransaction(previous_page)
        self.transac_pg.show()
        self.close()
    
    def show_view_acc(self):
        previous_page = Ui()
        self.view_pg = loadAccount(previous_page)
        self.view_pg.show() 
        self.close()

    def show_report(self):
        previous_page = Ui()
        self.view_pg = loadReport(previous_page)
        self.view_pg.show()
        self.close()

    def show_acc_history(self):
        previous_page = Ui()
        self.history_pg = loadAcc_History(previous_page)
        self.history_pg.show()
        self.close()

class loadTransaction(QtWidgets.QMainWindow):
    def __init__(self,previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserTransaction.ui', self)
        self.previous_page = previous_page
        self.pushButton_2.clicked.connect(self.create_acc)
        self.pushButton_3.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()

    def create_acc(self):
        previous_page = self
        self.create_pg = CreateAccount(previous_page)
        self.create_pg.show()
        self.close()
    pass

class loadAccount(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserAccounts.ui', self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.createAcc)
        self.pushButton_2.clicked.connect(self.showAccs)
        self.pushButton_3.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()

    def createAcc(self):
        previous_page = self
        self.create_pg = CreateAccount(previous_page)
        self.create_pg.show()
        self.close()

    def showAccs(self):
        previous_page = self
        self.acc_pg = loadViewAcc(previous_page)
        self.acc_pg.show()
        self.close()
    pass

class loadViewAcc(QtWidgets.QMainWindow):
    def __init__(self, prev):
        super().__init__()
        uic.loadUi('./UIs/UserViewAccounts.ui', self)
        self.previous_page = prev
        self.pushButton.clicked.connect(self.show_acc_history)
        self.pushButton_2.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()
    
    def show_acc_history(self):
        previous_page = self
        self.history_pg = loadAcc_History(previous_page)
        self.history_pg.show()
        self.close()
    pass

class loadReport(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/ReportPage.ui', self)
        self.previous_page = previous_page
        self.pushButton_2.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()
    pass


class loadAcc_History(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserViewAccountHistory.ui', self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()
    pass

class CreateAccount(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserCreateAccount.ui', self)
        self.previous_page = previous_page
        self.pushButton_2.clicked.connect(self.goback)

    def goback(self):
        self.previous_page.show()
        self.close()
    pass

        
class AdminMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./UIs/AdminMain.ui', self)
        self.pushButton.clicked.connect(self.show_users)
        self.pushButton_2.clicked.connect(self.show_reports)
        self.logoutButton.clicked.connect(self.logout)


    
    def logout(self):
        self.view_pg = Login()
        self.view_pg.show()
        self.close()
    

    def show_users(self):
        pass
    def show_reports(self):
        pass




# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)

window = Login() # Create an instance of our class
window.show() # Show the instance
app.exec() # Start the application