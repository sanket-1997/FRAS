# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from rec_interface import  Ui_RecognizeWindow
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from passlib.hash import sha256_crypt

class Ui_MainWindow(object):
    
   
    
    
    def login_button(self):
        ### Retrieve user from the database
         if len(self.edit_text_user_name.text()) > 0 and len(self.edit_text_password.text()) > 0:
        
            db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
            cursor = db.cursor()
            name=self.edit_text_user_name.text()
            password = self.edit_text_password.text()
            
            cursor.execute("SELECT Password FROM teacher_details WHERE UserName = %s",(name,))
            
            data = cursor.fetchone();
            
            if data:
                if sha256_crypt.verify(password,data[0]):
                    print('login')
                   
       
                    cursor.execute("DELETE FROM session_details WHERE t_id = 1")
                    db.commit()
                    cursor.execute("INSERT INTO session_details VALUES (1 , %s )",(name,))
                    db.commit()
                    cursor.close()
                    db.close()
                    self.window = QtWidgets.QMainWindow()
                    self.ui = Ui_RecognizeWindow()
                    self.ui.setupUi(self.window)
                    self.ui.populate_course(1)
                    
                    MainWindow.hide()
                    self.window.show()
                    
                else:
                     QMessageBox().information(None,"Info","Wrong Password!")
            else:
                 QMessageBox().information(None,"Info","Wrong User Name!")
            
            
            
            
          
        
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(529, 284)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.edit_text_user_name = QtWidgets.QLineEdit(self.centralwidget)

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
        self.edit_text_password = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_text_password.setGeometry(QtCore.QRect(180, 160, 331, 41))
        self.edit_text_password.setEchoMode(QtWidgets.QLineEdit.Password)
       
        font = QtGui.QFont()
        font.setPointSize(15)
        self.edit_text_password.setFont(font)
        self.edit_text_password.setObjectName("edit_text_password")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 230, 101, 41))
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
        self.pushButton.setText(_translate("MainWindow", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

