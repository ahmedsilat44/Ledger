import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QTableWidget,QTableWidgetItem
import pyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-6JOJPQM'
DATABASE_NAME = 'AccountingHuDb'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    uid=<hu>;
    
"""
connection = odbc.connect(connection_string)
print('Connected to the database')
# print('Connection:', connection)

# get all data from user table
cursor = connection.cursor()
cursor.execute('SELECT * FROM [Users]')
for row in cursor.fetchall():
    print(row)



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
        # check if id is a number
        if(id.isdigit()):
            id = int(id)
        else:
            id = 0
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
                username = ''
                username = user[1]
                username = username.lower()
                if (username.find('admin') != -1):
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
            #  Get the latest user added by selecting max user id
            cursor.execute(f"Select max(User_ID) from Users")
            user_id = cursor.fetchone()
            #alert
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Signup Successful')
            message_box.setText(f'User Registered Successfully, User id = { user_id[0]}')
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
        self.view_pg = UserReport(previous_page)
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
            # self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)
        else:
            cursor = connection.cursor()
            cursor.execute(f"SELECT Account_ID,Account_Name,Account_Type,Created_At,Balance FROM [Accounts] where User_ID = {Logged_in_userID} and Account_Type = '{account_type}'")
            # self.tableWidget.clear()
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
        self.month = 1
        self.MonthComboBox.currentTextChanged.connect(self.updateMonth)
        self.previous_page = previous_page
        self.pushButton_2.clicked.connect(self.goback)
        self.reportTypeComboBox.currentTextChanged.connect(self.update_label)
        self.pushButton.clicked.connect(self.generate_report)
        self.year = datetime.datetime.now().year
        
    
    def updateMonth(self):
        
        month = self.MonthComboBox.currentText()
        month = month.lower()
        match month:
            case 'january':
                self.month = 1
            case 'february':
                self.month = 2
            case 'march':
                self.month = 3
            case 'april':
                self.month = 4
            case 'may':
                self.month = 5
            case 'june':
                self.month = 6
            case 'july':
                self.month = 7
            case 'august':
                self.month = 8
            case 'september':
                self.month = 9
            case 'october':
                self.month = 10
            case 'november':
                self.month = 11
            case 'december':
                self.month = 12

        

    def goback(self):
        self.previous_page.show()
        self.close()

    def update_label(self):
        type=self.reportTypeComboBox.currentText()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3.setRowCount(0)
        if type == 'Income Statement':
            self.incomeLabel_2.setText('Income')
            self.expenseLabel_2.setText('Expense')
            self.netRevenueLabel_2.setText('Net Revenue')
            self.incomeLineEdit_2.setText('')
            self.expenseLineEdit_2.setText('')
            self.netRevenueLineEdit_2.setText('')
        elif type == 'Cash Flow':
            self.incomeLabel_2.setText('Cash Inflow')
            self.expenseLabel_2.setText('Cash Outflow')
            self.netRevenueLabel_2.setText('Net Cash Flow')
            self.incomeLineEdit_2.setText('')
            self.expenseLineEdit_2.setText('')
            self.netRevenueLineEdit_2.setText('')
    
    def generate_report(self):
        self.incomeLineEdit_2.setText('')
        self.expenseLineEdit_2.setText('')
        self.netRevenueLineEdit_2.setText('')
        type=self.reportTypeComboBox.currentText()
        cursor = connection.cursor()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3.setRowCount(0)
        if type == 'Income Statement':
            cursor.execute(f"SELECT Description, Generated_At, Amount, Debit_Account_ID, Credit_Account_ID,Generated_At,(Select Category_Name from Categories where Category_ID=1) FROM Transactions WHERE Category_ID in ( select Category_ID from Categories where Category_Name = 'Income')and (Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} )or Credit_Account_ID in ( Select Account_ID from Accounts where User_ID= {Logged_in_userID})) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            # check if the query returns any data
            # if(cursor.rowcount == 0):
            #     message_box = QtWidgets.QMessageBox()
            #     message_box.setWindowTitle('Report Generation Failed')
            #     message_box.setText('Not Enough Data')
            #     message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            #     message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            #     message_box.exec()
            #     return
            
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget_3.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
            
                    self.tableWidget_3.setItem(row_index, col_index, item)
            
            cursor.execute(f"SELECT Description, Generated_At, Amount, Debit_Account_ID, Credit_Account_ID,Generated_At,(Select Category_Name from Categories where Category_ID=2) FROM Transactions WHERE Category_ID in ( select Category_ID from Categories where Category_Name = 'Expense')and (Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} )or Credit_Account_ID in ( Select Account_ID from Accounts where User_ID= {Logged_in_userID})) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget_2.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget_2.setItem(row_index, col_index, item)

            # set label texts according to the sum of the amounts in the table using query and get transactions from the month selected and this year
            cursor.execute(f"SELECT coalesce(SUM(Amount),0) FROM Transactions WHERE Category_ID in ( select Category_ID from Categories where Category_Name = 'Income')and (Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} )or Credit_Account_ID in ( Select Account_ID from Accounts where User_ID= {Logged_in_userID})) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            income = cursor.fetchone()
            cursor.execute(f"SELECT coalesce(SUM(Amount),0) FROM Transactions WHERE Category_ID in ( select Category_ID from Categories where Category_Name = 'Expense')and (Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} )or Credit_Account_ID in ( Select Account_ID from Accounts where User_ID= {Logged_in_userID})) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            expense = cursor.fetchone()
            net_revenue = income[0] - expense[0]
            self.incomeLineEdit_2.setText(str(income[0]))
            self.expenseLineEdit_2.setText(str(expense[0]))
            self.netRevenueLineEdit_2.setText(str(net_revenue))

            

            # insert query to add data to Report table which has columns [ReportID] ,[ReportType],[ReportMonth],[GeneratedAt],[User_ID],[Income/CashIn],[Expense/CashOut],[NetRevenue/NetCashFlow] based on the type of report
            ## check if report already exists then update it else insert it
            cursor.execute(f"SELECT * FROM [Reports] WHERE ReportType = '{type}' AND ReportMonth = '{self.MonthComboBox.currentText()} {self.year}' AND User_ID = {Logged_in_userID}")
            if cursor.fetchone():
                cursor.execute(f"UPDATE [Reports] SET [Income/CashIn] = {income[0]}, [Expense/CashOut] = {expense[0]}, [NetRevenue/NetCashFlow] = {net_revenue} WHERE ReportType = '{type}' AND ReportMonth = '{self.MonthComboBox.currentText()} {self.year}' AND User_ID = {Logged_in_userID}")
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Report Generated')
                message_box.setText('Report Details Updated Successfully')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
            else:
                cursor.execute(f"INSERT INTO [Reports] (ReportType,ReportMonth,GeneratedAt,User_ID,[Income/CashIn],[Expense/CashOut],[NetRevenue/NetCashFlow]) Values ('{type}','{self.MonthComboBox.currentText()} {self.year}',GETDATE(),{Logged_in_userID},{income[0]},{expense[0]},{net_revenue})")
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Report Generated')
                message_box.setText('Report Generated Successfully')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()



        elif type == 'Cash Flow':
            cursor.execute(f"SELECT Description, Generated_At, Amount, Debit_Account_ID, Credit_Account_ID,Generated_At,(Select Category_Name from Categories where Category_ID in (Select Category_ID from Transactions t where t.Transaction_ID = Transactions.Transaction_ID)) FROM Transactions WHERE Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} and (Account_Name like '%Cash%' or Account_Name like '%cash%' )  ) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            # if(cursor.rowcount == 0):
            #     message_box = QtWidgets.QMessageBox()
            #     message_box.setWindowTitle('Report Generation Failed')
            #     message_box.setText('Not Enough Data')
            #     message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            #     message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            #     message_box.exec()
            #     return
            
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget_3.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget_3.setItem(row_index, col_index, item)
            cursor.execute(f"SELECT Description, Generated_At, Amount, Debit_Account_ID, Credit_Account_ID,Generated_At,(Select Category_Name from Categories where Category_ID in (Select Category_ID from Transactions t where t.Transaction_ID = Transactions.Transaction_ID)) FROM Transactions WHERE Credit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} and (Account_Name like '%Cash%' or Account_Name like '%cash%' )  ) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.tableWidget_2.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget_2.setItem(row_index, col_index, item)
        
            # set label texts according to the sum of the amounts in the table using query
            cursor.execute(f"SELECT coalesce(SUM(Amount),0) FROM Transactions WHERE Debit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} and (Account_Name like '%Cash%' or Account_Name like '%cash%' )  ) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            cash_inflow = cursor.fetchone()
            cursor.execute(f"SELECT coalesce(SUM(Amount),0) FROM Transactions WHERE Credit_Account_ID in ( Select Account_ID from Accounts where User_ID = {Logged_in_userID} and (Account_Name like '%Cash%' or Account_Name like '%cash%' )  ) and MONTH(Generated_At) = {self.month} and YEAR(Generated_At) = {self.year}")
            cash_outflow = cursor.fetchone()
            net_cash_flow = cash_inflow[0] - cash_outflow[0]
            self.incomeLineEdit_2.setText(str(cash_inflow[0]))
            self.expenseLineEdit_2.setText(str(cash_outflow[0]))
            self.netRevenueLineEdit_2.setText(str(net_cash_flow))
            

            # insert query to add data to Report table which has columns [ReportID] ,[ReportType],[ReportMonth],[GeneratedAt],[User_ID],[Income/CashIn],[Expense/CashOut],[NetRevenue/NetCashFlow] based on the type of report
            ## check if report already exists then update it else insert it

            cursor.execute(f"SELECT * FROM [Reports] WHERE ReportType = '{type}' AND ReportMonth = '{self.MonthComboBox.currentText()} {self.year}' AND User_ID = {Logged_in_userID}")
            if cursor.fetchone():
                cursor.execute(f"UPDATE [Reports] SET [Income/CashIn] = {cash_inflow[0]}, [Expense/CashOut] = {cash_outflow[0]}, [NetRevenue/NetCashFlow] = {net_cash_flow} WHERE ReportType = '{type}' AND ReportMonth = '{self.MonthComboBox.currentText()} {self.year}' AND User_ID = {Logged_in_userID}")
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Report Generated')
                message_box.setText('Report Details Updated Successfully')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
            else:
                cursor.execute(f"INSERT INTO [Reports] (ReportType,ReportMonth,GeneratedAt,User_ID,[Income/CashIn],[Expense/CashOut],[NetRevenue/NetCashFlow]) Values ('{type}','{self.MonthComboBox.currentText()} {self.year}',GETDATE(),{Logged_in_userID},{cash_inflow[0]},{cash_outflow[0]},{net_cash_flow})")
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Report Generated')
                message_box.setText('Report Generated Successfully')
                message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                message_box.exec()
        connection.commit()

        


        

    pass

class UserReport(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserReports.ui', self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.generate_report)
        self.pushButton_2.clicked.connect(self.show_report)
        self.pushButton_3.clicked.connect(self.goback)


    def goback(self):
        self.previous_page.show()
        self.close()
        
    def generate_report(self):
        previous_page = self
        self.report_pg = loadReport(previous_page)
        self.report_pg.show()
        self.close()

    def show_report(self):
        previous_page = self
        self.report_pg = UserViewReports(previous_page)
        self.report_pg.show()
        self.close()


class UserViewReports(QtWidgets.QMainWindow):
    def __init__(self, previous_page):
        super().__init__()
        uic.loadUi('./UIs/UserViewReports.ui', self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.goback)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [Reports] WHERE User_ID = {Logged_in_userID}")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
    
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
        self.acc_id=account_id
        cursor=connection.cursor()
        cursor.execute(f"select Transaction_ID,Generated_At,Amount,Description,Debit_Account_ID,Credit_Account_ID, (select Category_Name from Categories where Category_ID = Transactions.Category_ID  ) from Transactions where  Debit_Account_ID = {self.acc_id} or Credit_Account_ID = {self.acc_id}")
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        cursor.execute(f"SELECT * FROM [Accounts] WHERE Account_ID = {self.acc_id}")
        acc=cursor.fetchone()
        self.usernameLineEdit.setText(acc[1])
        self.accountTypeLineEdit.setText(acc[2])
        self.createdAtLineEdit.setText(acc[4])
        self.accountBalanceLineEdit.setText(str(acc[3]))

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
        self.pushButton_2.clicked.connect(self.show_transac)
        self.logoutButton.clicked.connect(self.logout)
        self.pushButton_3.clicked.connect(self.show_report)


    
    def logout(self):
        self.view_pg = Login()
        self.view_pg.show()
        self.close()
    

    def show_users(self):
        previous_page=AdminMain()
        self.user_view=AdminUserView(previous_page)
        self.user_view.show()
        self.close()
        
    def show_transac(self):
        previous_page=AdminMain()
        self.view_transac=AdminTransac(previous_page)
        self.view_transac.show()
        self.close()

    def show_report(self):
        previous_page = AdminMain()
        self.view_pg = AdminReport(previous_page)
        self.view_pg.show()
        self.close()

class AdminUserView(QtWidgets.QMainWindow):
    def __init__(self,previous_page):
        super().__init__()
        uic.loadUi('./UIs/AdminUserView.ui',self)
        self.previous_page = previous_page
        self.pushButton.clicked.connect(self.goback)
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor= connection.cursor()
        cursor.execute("select * from Users where User_Name != 'admin'")
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
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor.execute("select * from Users where User_Name != 'admin'")
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
        # self.tableWidget.clear()
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
        cursor.execute("select * from Users where User_Name != 'admin'")
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
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def goback(self):
        self.previous_page.show()
        self.close()

class AdminReport(QtWidgets.QMainWindow):
    def __init__(self,previous_page):
        super().__init__()
        self.previous_page = previous_page
        uic.loadUi('./UIs/AdminViewReports.ui',self)
        self.pushButton.clicked.connect(self.goback)
        self.tableWidget.setRowCount(0)
        cursor= connection.cursor()
        cursor.execute("select * from Reports")
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
