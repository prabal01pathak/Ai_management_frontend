import sys
# import qmainwindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QStackedWidget
from libs.resources import *
# import uiloader
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from labelImg import main
import requests
import json
import time
from thread_worker import Worker
import os
from frames_collection.dashboard import MainWindow

server_url = "http://localhost:8000"
image_path = "./assets/background_image.jpg"
path = os.path.abspath(image_path)

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("./uifiles/login.ui", self)
        self.setWindowTitle("Login")
        self.loginBtn.clicked.connect(self.emitter_object)
        self.server_url = server_url
        self.threadpool = QtCore.QThreadPool()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        #self.centralwidget.setStyleSheet("#centralwidget{background-image: url(C:/Users/hp/ai_managementLabeling/assets/background_image.jpg);}")
        #self.centralWidget.addStyleSheet("#centralwidget{background-image: url(C:/Users/hp/ai_managementLabeling/assets/background_image.jpg);}")
        #MainWindow.setStyleSheet("background-image: url(:/assets/background_image.jpg)")

    def login_user(self, *args, **kwargs):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        form_data = {
            'username': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.server_url + '/token', data=form_data, headers=headers)
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
        print(result)
        if 'access_token' in result:
            print("Authenticated")
            self.access_token = result['access_token']
            print(self.access_token)
            self.close()
            self.app = MainWindow(app, self.access_token, stacked_widget)
            stacked_widget.addWidget(self.app)
            stacked_widget.setCurrentWidget(self.app)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    stacked_widget.addWidget(LoginWindow())
    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()
    # show maximized
    stacked_widget.showMaximized()
    sys.exit(app.exec_())


