from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from labelImg import main
import requests
import json
from thread_worker import Worker
import os

server_url = "http://localhost:8000"

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

        self.login_button.clicked.connect(self.emitter_object)
        self.server_url = server_url
        self.threadpool = QtCore.QThreadPool()

    def login_user(self, *args, **kwargs):
        username = self.id_button.text()
        password = self.password.text()
        form_data = {
            'username': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.server_url + '/auth/token', data=form_data, headers=headers)
            self.response_json = response.json()
            if response.status_code == 200:
                self.access_token = self.response_json['access_token']
                with open('access_token.json', 'w') as f:
                    json.dump(self.response_json, f)
            else:
                print('error')
        except Exception as e:
            print(e)
            self.response_json = {'error': 'error'}
        return self.response_json

    def emitter_object(self):
        self.emitter = Worker(self.login_user)
        self.emitter.signals.finished.connect(self.show_app)
        self.threadpool.start(self.emitter)

    def show_app(self):
        result = self.response_json
        if 'access_token' in result:
            print("Authenticated")
            self.access_token = result['access_token']
            login.close()
            main(app, self.access_token)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.login_button.setText(_translate("MainWindow", "login"))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    print(os.path.isfile('access_token.json'))
    if not os.path.isfile('access_token.json'):
        login = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(login)
        login.show()
        sys.exit(app.exec_())
    else:
        with open('access_token.json', 'r') as f:
            result = json.load(f)
        main(app, result['access_token'])
        sys.exit(app.exec_())
