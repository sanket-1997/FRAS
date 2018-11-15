# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from passlib.hash import sha256_crypt


class Ui_MainWindow(object):
    
   
        
    def login_button(self):
        
        if len(self.edit_text_user_name.toPlainText()) > 2 and len(self.edit_text_password.toPlainText()) > 7:
            ### save name and password in the database
            db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
            cursor = db.cursor()
            
            password = sha256_crypt.hash(self.edit_text_password.toPlainText())
            name = self.edit_text_user_name.toPlainText()
            try:
                
                cursor.execute("INSERT INTO teacher_details (UserName, Password) VALUES (%s, %s)",(name,password))
                db.commit()
                QMessageBox().information(None,"Info","New User Created!")
            except:
                QMessageBox().information(None,"Info","User Name already exists!")
                
            cursor.close()
            db.close()
            
            
            #msg.about(None,"Info","New User Created!")
            self.edit_text_user_name.setText("")
            self.edit_text_password.setText("")
        else:
            QMessageBox().warning(None,"Warning","All Fields are mandatory and password must be atleast 8 character long!!")
            
            
            
        
          #print(len(self.edit_text_user_name.toPlainText()))  
        
        
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(529, 284)
       
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.edit_text_user_name = QtWidgets.QTextEdit(self.centralwidget)
        self.edit_text_user_name.setGeometry(QtCore.QRect(180, 60, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.edit_text_user_name.setFont(font)
        self.edit_text_user_name.setObjectName("edit_text_user_name")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(20, 170, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.edit_text_password = QtWidgets.QTextEdit(self.centralwidget)
        self.edit_text_password.setGeometry(QtCore.QRect(180, 160, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.edit_text_password.setFont(font)
        self.edit_text_password.setObjectName("edit_text_password")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 230,170, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.login_button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "User Name"))
        self.label2.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Create User"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

