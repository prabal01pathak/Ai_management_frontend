from PyQt5 import QtCore, QtGui, QtWidgets
from labelImg import main
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(558, 383)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(240, 250, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(220, 180, 113, 21))
        self.password.setObjectName("password")
        self.id = QtWidgets.QLineEdit(Dialog)
        self.id.setGeometry(QtCore.QRect(220, 140, 113, 21))
        self.id.setObjectName("id")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.login)
    def login(self):
        id = self.id.text()
        password = self.password.text()
        if id == "admin" and password == "admin":
            # exit the login screen
            sys.exit()
            main()
        else:
            print("Invalid Login")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "login"))
        self.password.setPlaceholderText(_translate("Dialog", "password"))
        self.id.setPlaceholderText(_translate("Dialog", "Login Id"))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
