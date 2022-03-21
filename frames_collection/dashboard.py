from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from labelImg import main
from thread_worker import Worker
import requests

server_url = 'http://localhost:8000'

class MainWindow(QMainWindow):
    def __init__(self, app, access_token, stacked_widget, parent=None):
        super(MainWindow, self).__init__()
        loadUi('./uifiles/dashboard.ui', self)
        self.setWindowTitle('Dashboard')
        self.firstProjectBtn.clicked.connect(self.show_next_frame)
        self.accountButton.clicked.connect(self.back_to_main)
        self.stacked_widget = stacked_widget
        self.access_token = access_token
        self.app = app
        #self.emitter_object()
        self.get_project_details()
        self.add_project_details()

    def get_project_details(self,*args,**kwargs):
        print("requesting project details")
        headers = {'Authorization': 'Bearer ' + self.access_token}
        try: 
            response = requests.get(server_url + '/projects', headers=headers)
            self.response_data = response.json()
        except Exception as e:
            print(e)
            self.response_data = None
        return self.response_data

    def emitter_object(self):
        emitter = Worker(self.get_project_details)
        emitter.signals.finished.connect(self.add_project_details)
        threadpool = QtCore.QThreadPool()
        threadpool.start(emitter)

    def add_project_details(self):
        _translate = QtCore.QCoreApplication.translate
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        if self.response_data:
            for key, value in self.response_data.items():
                # generate dinamic variable names
                projectBtn = QPushButton(self.firstProject)
                projectBtn.setFont(font)
                projectBtn.setObjectName(str(key))
                projectBtn.setText(_translate("MainWindow", self.response_data[key]['project_name']))
                projectBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                projectBtn.clicked.connect(lambda: self.show_next_frame(projectBtn.objectName()))
                annotationDone = QLabel(self.firstProject)
                annotationDone.setFont(font)
                annotationDone.setObjectName(str(self.response_data[key]['annotations_done']))
                annotationDone.setText(_translate("MainWindow", str(self.response_data[key]['annotations_done'])))
                annotationDone.setAlignment(QtCore.Qt.AlignCenter)
                NoOfImages = QLabel(self.firstProject)
                NoOfImages.setFont(font)
                NoOfImages.setObjectName(str(self.response_data[key]['no_of_images']))
                NoOfImages.setText(_translate("MainWindow", str(self.response_data[key]['no_of_images'])))
                #self.NoOfImages.setText(_translate("MainWindow", str(self.response_data[key]['no_of_images']))
                NoOfImages.setAlignment(QtCore.Qt.AlignCenter)
                self.projectLayout.addWidget(projectBtn, int(key),0,1,1)
                self.projectLayout.addWidget(annotationDone, int(key),1,1,1)
                self.projectLayout.addWidget(NoOfImages, int(key),2,1,1)

    def show_next_frame(self, project_id):
        self.stacked_widget.close()
        print("project id: ", project_id)
        main(self.app, self.access_token, project_id)

    def back_to_main(self):
        self.stacked_widget.setCurrentIndex(0)



