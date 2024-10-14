from PyQt6 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self,):
        super(Ui,self).__init__()
        uic.loadUi('UserMain.ui',self)
        

  
        self.pushButton_2.clicked.connect(self.show_transaction)
        self.pushButton.clicked.connect(self.show_view_acc)
        self.pushButton_3.clicked.connect(self.show_report)
    
    
    
    def show_transaction(self):
        self.transac_pg = loadTransaction()
        self.transac_pg.show()   
    
    def show_view_acc(self):
        self.view_pg = loadViewAcc()
        self.view_pg.show() 

    def show_report(self):
        self.view_pg = loadReport()
        self.view_pg.show()

    def show_acc_history(self):
        self.history_pg = loadAcc_History()
        self.history_pg.show()

class loadTransaction(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UserTransaction.ui', self)

        self.pushButton_2.clicked.connect(self.create_acc)
    def create_acc(self):
        self.create_pg = CreateAccount()
        self.create_pg.show()
    pass

class loadViewAcc(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UserViewAccounts.ui', self)
        
        self.pushButton.clicked.connect(self.show_acc_history)
        self.pushButton_2.clicked.connect(self.close)
    def show_acc_history(self):
        self.history_pg = loadAcc_History()
        self.history_pg.show()
    pass

class loadReport(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ReportPage.ui', self)
    pass

class loadAcc_History(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UserViewAccountHistory.ui', self)

        self.pushButton.clicked.connect(self.close)
    pass

class CreateAccount(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UserCreateAccount.ui', self)
    pass
app  = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec()
