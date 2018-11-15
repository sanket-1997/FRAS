# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rec_recognize.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QInputDialog, QLineEdit,QMessageBox
import mysql.connector
import os
import sys
from passlib.hash import sha256_crypt



class Ui_RecognizeWindow(object):
    
    link=0;
    
    def logout(self):  
        db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
        cursor = db.cursor()      
        cursor.execute("DELETE FROM session_details WHERE t_id = 1")
        db.commit()
        cursor.close()
        db.close()
        sys.exit()
        
        
    def change_password(self):
        text, okPressed = QInputDialog.getText(None, "New Password","Enter New Password", QLineEdit.Password, "")
        if okPressed :
            if len(text)>7:
                 print(text)
                 db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
                 cursor = db.cursor()
                 password = sha256_crypt.hash(text)
                 
                 cursor.execute("UPDATE teacher_details SET Password = %s WHERE UserName = %s",(password,self.label_5.text()))
                 db.commit()
                 QMessageBox().information(None,"Info","Password is changed!")
                 
                 cursor.close()
                 db.close()
            
                 
                
            else:
                QMessageBox().warning(None,"Warning","Password must be atleast 8 character long!!")
           
            
    
    def populate_course(self , x):
        self.link = x
        
        print(self.link)
        db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM course_details")
        data = cursor.fetchall()
        for i in range(1,9):
            self.comboBoxSemester.addItem(str(i))
        
        for singleData in data:
            self.comboBoxCourse.addItem(str(singleData[1]))
                
        cursor.execute("SELECT UserName FROM session_details WHERE t_id = 1")   
        name = cursor.fetchone()
        try:
            self.label_5.setText(name[0])
        except:
            self.label_5.setText("unknown")
        cursor.close()
        db.close()
    
    
    def start_attendance(self):
        db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
        cursor = db.cursor()
        cursor.execute("SELECT course_id FROM course_details WHERE course_name = %s",(self.comboBoxCourse.currentText(),))
        course_id = cursor.fetchone()
        sql = "UPDATE selection_of_course SET course_id = %s, semester = %s WHERE id = 1"
        cursor.execute(sql,(course_id[0],self.comboBoxSemester.currentText()))
        db.commit()
        cursor.close()
        db.close()
        os.system('python recognize.py')
        
        
        
    def view_attendance(self):
        db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )
        cursor = db.cursor()
        
        cursor.execute("SELECT student_id , student_name FROM student_details WHERE semester = %s",(self.comboBoxSemester.currentText(),))
        data = cursor.fetchall()   #### fetch students
        cursor.execute("SELECT course_id FROM course_details WHERE course_name = %s",(self.comboBoxCourse.currentText(),))
        course_id = cursor.fetchone()   #### fetch course id
        cursor.execute("SELECT Count(DISTINCT date_held) FROM attendance_tracker where course_id ='%s'",(course_id[0],))
        days = cursor.fetchone()  #### this is for total attendance
        print(str(days[0]))
        individual_attendance = []
        
        for person in data:
            cursor.execute("SELECT Count(DISTINCT date_held) FROM attendance_tracker where course_id ='%s' and student_id ='%s'",
                           (course_id[0],person[0])
                           )# result of individual person
            individual_days = cursor.fetchone()
            individual_attendance.append(individual_days[0])
        
        ###club the data
    
        self.tableWidget.setRowCount(0)
        try:
            for i in range(0 , len(data)):
                self.tableWidget.insertRow(i)
                for j in range(0 , 3):
                        if j == 2:
                            percent = (individual_attendance[i]/days[0])*100
                            percent = "{:.2f}".format(percent)
                            self.tableWidget.setItem(i,j,QTableWidgetItem(str(percent)+"%"))
                        else:    
                            self.tableWidget.setItem(i,j,QTableWidgetItem(str(data[i][j])))
            
        except:
            print('No data')
            
        
        
        print(individual_attendance)
        
        cursor.close()
        db.close()
        
        
    
    def setupUi(self, RecognizeWindow):
        RecognizeWindow.setObjectName("RecognizeWindow")
        RecognizeWindow.resize(756, 349)
        self.centralwidget = QtWidgets.QWidget(RecognizeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBoxCourse = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCourse.setGeometry(QtCore.QRect(170, 80, 161, 31))
        self.comboBoxCourse.setObjectName("comboBoxCourse")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(520, 10, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 85, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBoxSemester = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSemester.setGeometry(QtCore.QRect(170, 140, 161, 31))
        self.comboBoxSemester.setObjectName("comboBoxSemester")
        self.btnStartAttendance = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartAttendance.setGeometry(QtCore.QRect(10, 210, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.btnStartAttendance.setFont(font)
        self.btnStartAttendance.setObjectName("btnStartAttendance")
        self.btnStartAttendance.clicked.connect(self.start_attendance)
        self.btnViewAttendance = QtWidgets.QPushButton(self.centralwidget)
        self.btnViewAttendance.setGeometry(QtCore.QRect(200, 210, 131, 31))
        self.btnViewAttendance.clicked.connect(self.view_attendance)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.btnViewAttendance.setFont(font)
        self.btnViewAttendance.setObjectName("btnViewAttendance")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(380, 80, 371, 261))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(('Roll No.','Name','Attendance'))
        
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 761, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(340, 50, 20, 341))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.btnLogout = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogout.setGeometry(QtCore.QRect(10, 280, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.btnLogout.setFont(font)
        self.btnLogout.setObjectName("btnLogout")
        self.btnChangePassword = QtWidgets.QPushButton(self.centralwidget)
        self.btnChangePassword.setGeometry(QtCore.QRect(200, 280, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.btnChangePassword.setFont(font)
        self.btnChangePassword.setObjectName("btnChangePassword")
        self.btnChangePassword.clicked.connect(self.change_password)
        
        self.btnLogout.clicked.connect(self.logout)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 50, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 351, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setObjectName("label_5")
        RecognizeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RecognizeWindow)
        QtCore.QMetaObject.connectSlotsByName(RecognizeWindow)

    def retranslateUi(self, RecognizeWindow):
        _translate = QtCore.QCoreApplication.translate
        RecognizeWindow.setWindowTitle(_translate("RecognizeWindow", "MainWindow"))
        self.label.setText(_translate("RecognizeWindow", "Control Panel"))
        self.label_2.setText(_translate("RecognizeWindow", "Course Selection"))
        self.label_3.setText(_translate("RecognizeWindow", "Semester"))
        self.btnStartAttendance.setText(_translate("RecognizeWindow", "Start Attendance"))
        self.btnViewAttendance.setText(_translate("RecognizeWindow", "View Attendance"))
        self.btnLogout.setText(_translate("RecognizeWindow", "Logout"))
        self.btnChangePassword.setText(_translate("RecognizeWindow", "Change Password"))
        self.label_4.setText(_translate("RecognizeWindow", "Attendance Details"))
        self.label_5.setText(_translate("RecognizeWindow", "Welcome"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RecognizeWindow = QtWidgets.QMainWindow()
    ui = Ui_RecognizeWindow()
    ui.setupUi(RecognizeWindow)
    ui.populate_course()
    RecognizeWindow.show()
        
    sys.exit(app.exec_())

