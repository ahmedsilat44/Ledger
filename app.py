import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QTableWidget,QTableWidgetItem
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
cursor.execute('SELECT * FROM [Accounts]')
for row in cursor.fetchall():
    print("Account Name : " + row[1])



import datetime
# Returns the current local date

#variable so that when back button is pressed makes sure that the previous page is loaded

global Logged_in_userID

Logged_in_userID = 0




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
                global Logged_in_userID
                Logged_in_userID = user[0]
                print(Logged_in_userID)
                if (user[0] == 6):
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
        global Logged_in_userID
        self.pushButton_2.clicked.connect(self.create_acc)
        self.pushButton_3.clicked.connect(self.goback)
        debitCombo = self.debitAccountComboBox
        creditCombo = self.creditAccountComboBox
        categoryCombo = self.categoryComboBox
        debitCombo.clear()
        creditCombo.clear()
        categoryCombo.clear()
    

        self.pushButton.clicked.connect(self.create_transaction)
        debitCombo.currentIndexChanged.connect(self.debit_account_changed)
        cursor = connection.cursor()
        print(Logged_in_userID , "Logged in user ID")
        cursor.execute(f"SELECT * FROM [Accounts] where User_ID = {Logged_in_userID}")
        accounts = cursor.fetchall()
        for account in accounts:
            debitCombo.addItem(account[1],account)

        cursor.execute(f"Select * from Categories")
        categories = cursor.fetchall()
        for category in categories:
            categoryCombo.addItem(category[1],category)
        

        
    def debit_account_changed(self):
        debitCombo = self.debitAccountComboBox
        creditCombo = self.creditAccountComboBox
        creditCombo.clear()
        debit_account = debitCombo.currentData()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Accounts] where User_ID = {Logged_in_userID} and Account_ID != {debit_account[0]}")
        accounts = cursor.fetchall()
        for account in accounts:
            print(account[1])
            creditCombo.addItem(account[1],account)

    def goback(self):
        self.previous_page.show()
        self.close()

    def create_acc(self):
        previous_page = self
        self.create_pg = CreateAccount(previous_page)
        self.create_pg.show()
        self.close()
    
    def create_transaction(self):
        debitCombo = self.debitAccountComboBox
        creditCombo = self.creditAccountComboBox
        categoryCombo = self.categoryComboBox
        print(debitCombo.currentData()[0], "Debit Account ID", creditCombo.currentData()[0], "Credit Account ID")
        print(debitCombo.currentData()[1], "Debit Account Name", creditCombo.currentData()[1], "Credit Account Name")

        amount = self.amountLineEdit.text()
        try:
            amount = float(amount)
        except:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Transaction Failed')
            message_box.setText('Amount must be a number')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        
        description = self.descriptionLineEdit.text()
        if not amount or not description:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Transaction Failed')
            message_box.setText('Amount and Description are required')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        cursor = connection.cursor()


        cursor.execute(f"INSERT INTO [Transactions] (Generated_At, Amount, Description, Debit_Account_ID, Credit_Account_ID, Category_ID ) Values (GETDATE(), {amount}, '{description}', {debitCombo.currentData()[0]}, {creditCombo.currentData()[0]}, {categoryCombo.currentData()[0]})")
        
        
        
        # add balance to both accounts depending on the category of account ( asset , equity , liability, revenue, expense)
        # get the account category of the account
        cursor.execute(f"SELECT * FROM [Accounts] WHERE Account_ID = {debitCombo.currentData()[0]}")
        debit_account = cursor.fetchone()
        match debit_account[2]:
            case 'Asset':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance + {amount} WHERE Account_ID = {debitCombo.currentData()[0]}")
            case 'Equity':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance - {amount} WHERE Account_ID = {debitCombo.currentData()[0]}")
            case 'Liability':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance - {amount} WHERE Account_ID = {debitCombo.currentData()[0]}")
            case 'Revenue':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance - {amount} WHERE Account_ID = {debitCombo.currentData()[0]}")
            case 'Expense':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance + {amount} WHERE Account_ID = {debitCombo.currentData()[0]}")

        # commit the changes
        connection.commit()

        cursor.execute(f"SELECT * FROM [Accounts] WHERE Account_ID = {creditCombo.currentData()[0]}")
        credit_account = cursor.fetchone()
        match credit_account[2]:
            case 'Asset':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance - {amount} WHERE Account_ID = {creditCombo.currentData()[0]}")
            case 'Equity':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance + {amount} WHERE Account_ID = {creditCombo.currentData()[0]}")
            case 'Liability':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance + {amount} WHERE Account_ID = {creditCombo.currentData()[0]}")
            case 'Revenue':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance + {amount} WHERE Account_ID = {creditCombo.currentData()[0]}")
            case 'Expense':
                cursor.execute(f"UPDATE [Accounts] SET Balance = Balance - {amount} WHERE Account_ID = {creditCombo.currentData()[0]}")
        
        connection.commit()

        #transaction committed result

        cursor.execute(f"Select max(Transaction_ID) from Transactions")
        transaction_id = cursor.fetchone()


        

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Transaction Successful')
        message_box.setText('Transaction Created Successfully, Transaction ID = ' + str(transaction_id[0]))
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()
        self.goback()

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
        cursor= connection.cursor()
        cursor.execute(f"SELECT Account_ID,Account_Name,Account_Type,Created_At,Balance FROM [Accounts] where User_ID = {Logged_in_userID} ")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

        #  filter the accounts based on the account type
        self.accountTypeComboBox.currentIndexChanged.connect(self.filter_accounts)


    def filter_accounts(self):
        # if selected filter is All, show all accounts
        accountTypeComboBox = self.accountTypeComboBox
        account_type = accountTypeComboBox.currentText()
        if account_type == 'All':
            cursor = connection.cursor()
            cursor.execute(f"SELECT Account_ID,Account_Name,Account_Type,Created_At,Balance FROM [Accounts] where User_ID = {Logged_in_userID}")
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)
        else:
            cursor = connection.cursor()
            cursor.execute(f"SELECT Account_ID,Account_Name,Account_Type,Created_At,Balance FROM [Accounts] where User_ID = {Logged_in_userID} and Account_Type = '{account_type}'")
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)
        


    def goback(self):
        self.previous_page.show()
        self.close()
    
    def show_acc_history(self):
        #  check if table widget has a selected row if it does show the account history
        if self.tableWidget.currentRow() == -1:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Account History Failed')
            message_box.setText('Select an account to view history')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            account_id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            previous_page = self
            self.history_pg = loadAcc_History(previous_page,account_id)
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
    def __init__(self, previous_page,account_id):
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
        self.pushButton.clicked.connect(self.create_account)

    def create_account(self):
        account_name = self.usernameLineEdit.text()
        account_type = self.accountTypeComboBox.currentText()
        descritpion = self.descriptionLineEdit.text()
        if not account_name or not account_type:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Account Creation Failed')
            message_box.setText('Account Name and Account Type are required')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO [Accounts] (Account_Name, Account_Type, Balance,Created_At, Description, User_ID) VALUES ('{account_name}', '{account_type}', 0, GETDATE(), '{descritpion}',  {Logged_in_userID})")
        connection.commit()
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Account Created')
        message_box.setText('Account Created Successfully')
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()
        

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
        previous_page=AdminMain()
        self.user_view=AdminUserView(previous_page)
        self.user_view.show()
        self.close()
        
    def show_reports(self):
        previous_page=AdminMain()
        self.view_transac=AdminTransac(previous_page)
        self.view_transac.show()
        self.close()

class AdminUserView(QtWidgets.QMainWindow):
    def __init__(self,previous_page):
        super().__init__()
        uic.loadUi('./UIs/AdminUserView.ui',self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.goback)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor= connection.cursor()
        cursor.execute("select * from Users where User_ID != 6")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

        #  Toggle the user approval status when the button is clicked and check if a cell is selected
        self.pushButton_2.clicked.connect(self.toggle_approval)

    def toggle_approval(self):
        print(self.tableWidget.currentRow())
        if self.tableWidget.currentRow() == -1:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Approval Failed')
            message_box.setText('Select a user to approve/disapprove')
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        user = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Users] WHERE User_ID = {user}")
        user = cursor.fetchone()
        if user[4] == True:
            cursor.execute(f"UPDATE [Users] SET Approved = 0 WHERE User_ID = {user[0]}")
        else:
            cursor.execute(f"UPDATE [Users] SET Approved = 1 WHERE User_ID = {user[0]}")
        connection.commit()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor.execute("select * from Users where User_ID != 6")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)


    def goback(self):
        self.previous_page.show()
        self.close()


class AdminTransac(QtWidgets.QMainWindow):
    def __init__(self,previous_page):
        super().__init__()
        uic.loadUi('./UIs/AdminTransactions.ui',self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.goback)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor= connection.cursor()
        cursor.execute("select Transaction_ID,Generated_At,Amount,Description,Debit_Account_ID,Credit_Account_ID, (select Category_Name from Categories where Category_ID = Transactions.Category_ID  ) from Transactions")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
                
        userFilterComboBox = self.userFilterComboBox
        userFilterComboBox.clear()
        userFilterComboBox.addItem("All")
        cursor.execute("select * from Users where User_ID != 6")
        for user in cursor.fetchall():
            userFilterComboBox.addItem(user[1], user)

        self.userFilterComboBox.currentIndexChanged.connect(self.filter_transactions)         
    
    
    def filter_transactions(self):
        userFilterComboBox = self.userFilterComboBox
        user = userFilterComboBox.currentData()
        cursor = connection.cursor()
        if user:
            cursor.execute(f"select Transaction_ID,Generated_At,Amount,Description,Debit_Account_ID,Credit_Account_ID, (select Category_Name from Categories where Category_ID = Transactions.Category_ID  ) from Transactions where  Debit_Account_ID in (select Account_ID from Accounts where User_ID = (select User_ID from Users where User_ID = {user[0]})) or Credit_Account_ID in (select Account_ID from Accounts where User_ID = (select User_ID from Users where User_ID = {user[0]}))")
        else:
            cursor.execute("select Transaction_ID,Generated_At,Amount,Description,Debit_Account_ID,Credit_Account_ID, (select Category_Name from Categories where Category_ID = Transactions.Category_ID  ) from Transactions")
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def goback(self):
        self.previous_page.show()
        self.close()

    

# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)

window = Login() # Create an instance of our class
window.show() # Show the instance
app.exec() # Start the application
