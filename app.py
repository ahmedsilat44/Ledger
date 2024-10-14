import sys
from PyQt6 import QtWidgets
from PyQt6 import uic

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

        # Event handling
    #     self.categoryComboBox.currentTextChanged.connect(self.update_ComboBox)
    #     self.authorNamePushButton.clicked.connect(self.authorNamePushButton_clicked)
    #     self.issuedCheckBox.clicked.connect(self.enableIssuance)
    #     self.clearLstBtn.clicked.connect(self.clearAuthorList)
    #     self.journalRadio.toggled.connect(self.journalCheck)
    #     self.okayBtn.clicked.connect(self.completeAddition)
    #     self.closeBtn.clicked.connect(self.close)

    # def close(self):
    #     self.close()

    # def completeAddition(self):
    #     if len(self.iSBNLineEdit.text()) <= 12 and  self.purchasedOnDateEdit.date() <= datetime.datetime.now() :
    #         if self.issuedCheckBox.isChecked():
    #             if self.issuedByLineEdit.text() == '' or self.issuedOnDateEdit.date() > datetime.datetime.now() or self.issuedOnDateEdit.date() >= self.purchasedOnDateEdit.date():
    #                 dlg = QtWidgets.QMessageBox(self)
    #                 dlg.setWindowTitle ( "Error" )
    #                 dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    #                 dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok )
    #                 dlg.setText ( "Please fill the Issued By field and make sure Issued On Date is lesser than or equal to today and greater than Purchased On Date" )
    #                 dlg . exec ()
    #                 return
            
    #         dlg = QtWidgets.QMessageBox(self)
    #         dlg.setWindowTitle ( "Success" )
    #         dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    #         dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok )
    #         dlg.setText ( " Book Added Successfully " )
    #         dlg . exec ()
    #     else:
    #         dlg = QtWidgets.QMessageBox(self)
    #         dlg.setWindowTitle ( "Success" )
    #         dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    #         dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok )
    #         dlg.setText ( "The length of ISBN or Purchased On Date is greater than today " )
    #         dlg . exec ()


    # def journalCheck(self):
    #     if self.journalRadio.isChecked() and self.authorNameList.count() > 0:
    #         self.authorNameList.clear()
    #         dlg = QtWidgets.QMessageBox(self)
    #         dlg.setWindowTitle ( "Error" )
    #         dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    #         dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok )
    #         dlg.setText ( " Journals can have no Author " )
    #         dlg . exec ()

    # def clearAuthorList(self):
    #     self.authorNameList.clear()


    # def authorNamePushButton_clicked(self):
    #     # print(self.authorNameLineEdit.text())
    #     if self.authorNameLineEdit.text() != '':
    #         self.authorNameList.addItem(self.authorNameLineEdit.text())

    # def enableIssuance(self):
    #     if self.issuedCheckBox.isChecked():
    #         self.issuedByLineEdit.setEnabled(True)
    #         self.issuedOnDateEdit.setEnabled(True)
    #         self.issuedByLineEdit.setReadOnly(False)
    #         self.issuedOnDateEdit.setReadOnly(False)
    #     else:
    #         self.issuedByLineEdit.setEnabled(False)
    #         self.issuedOnDateEdit.setEnabled(False)
        
    # def update_ComboBox(self, text):
    #     self.subCategoryComboBox.clear()
    #     if text == 'Database Systems':
    #         self.subCategoryComboBox.addItems(("ERD", "SQL", "OLAP", "Data Mining"))
    #     if text == 'OOP':
    #         self.subCategoryComboBox.addItems(("C++", "Java"))
    #     if text == 'Artificial Intelligence':
    #         self.subCategoryComboBox.addItems(("Machine Learning", "Robotics", "Computer Vision"))


# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)
window = Login() # Create an instance of our class
app.exec() # Start the application