from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from labelImg import main


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(360, 330, 75, 24))
        self.login_button.setObjectName("login_button")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(340, 280, 113, 21))
        self.password.setObjectName("password")
        self.id_button = QtWidgets.QLineEdit(self.centralwidget)
        self.id_button.setGeometry(QtCore.QRect(340, 220, 113, 21))
        self.id_button.setObjectName("id_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.login_button.clicked.connect(self.show_app)
    def show_app(self):
        self.id = self.id_button.text()
        self.passw = self.password.text()
        if self.id == 'admin' and self.passw == 'admin':
            login.close()
            main(app)
        else:
            print('error')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.login_button.setText(_translate("MainWindow", "login"))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(login)
    login.show()
    sys.exit(app.exec_())
