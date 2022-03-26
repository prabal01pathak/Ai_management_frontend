from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QGridLayout, 
    QVBoxLayout, 
    QHBoxLayout, 
    QComboBox, 
    QMessageBox, 
    QFileDialog,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from labelImg import main
from thread_worker import Worker
import requests
import copy
from widget import Ui_Form

server_url = 'http://localhost:8000'

class MainWindow(QMainWindow):
    def __init__(self, app, access_token, stacked_widget, parent=None):
        super(MainWindow, self).__init__()
        loadUi('./uifiles/dashboard.ui', self)
        self.setWindowTitle('Dashboard')
        self.accountButton.clicked.connect(self.back_to_main)
        self.stacked_widget = stacked_widget
        self.access_token = access_token
        self.app = app
        # add top bottom and left right shadow
        self.setGraphicsEffect(QGraphicsDropShadowEffect(self))
        # add shadow to all the widgets
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setBlurRadius(25)
        color  = QtGui.QColor(0, 0, 0, 150)
        shadow = color.darker(150)
        self.emitter_object()
        #self.get_project_details()
        #self.add_project_details()

        # add child Qframe shandow

    def getattr(self,name):
        self.name = name
        return self.name


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
        self.emitter = Worker(self.get_project_details, self.access_token)
        #self.emitter.signals.finished.connect(self.add_project_details)
        self.emitter.signals.finished.connect(self.add_widget)
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.start(self.emitter)
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def add_project_details_emitter(self):
        emitter = Worker(self.add_project_details)
        threadpool = QtCore.QThreadPool()
        threadpool.start(emitter)

    def add_widget(self):
        self.available_pushbuttons = {}
        j = 0
        if self.response_data:
            i = 0
            j = 0
            for key, value in self.response_data.items():
                project_name = self.response_data[key]['project_name']
                annotations_count = str(self.response_data[key]['annotations_done'])
                no_of_images = str(self.response_data[key]['no_of_images'])
                cardWidget = QWidget()
                cardWidgetClass = loadUi('./uifiles/widget.ui', cardWidget)
                cardWidgetClass.noOfImageValue.setText(no_of_images)
                cardWidgetClass.noOfAnnotationValue.setText(annotations_count)
                cardWidgetClass.projectName.setText(project_name)
                #self.cardWidgetClass.setupUi(self.cardWidget)
                print(i,j)
                cardWidget.setGraphicsEffect(self.effect)
                self.scrollAreaLayout.addWidget(cardWidget,i,j, 1, 1)
                self.available_pushbuttons[key] = cardWidgetClass.viewProjectBtn
                j += 1
                if j == 3:
                    j = 0
                    i += 1
                #if i == 3:
                #    break
            if len(self.available_pushbuttons) > 0:
                for key, value in self.available_pushbuttons.items():
                    value.clicked.connect(lambda state, key=key: self.show_next_frame(key))

    def add_project_details(self):
        print("adding project details")
        _translate = QtCore.QCoreApplication.translate
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.available_pushbuttons = {}
        if self.response_data:
            i = 0
            j = 0
            for key, value in self.response_data.items():
                project_name = self.response_data[key]['project_name']
                annotations_count = str(self.response_data[key]['annotations_done'])
                no_of_images = str(self.response_data[key]['no_of_images'])
                card1_2 = QtWidgets.QFrame(self.cardContainer)
                card1_2.setMinimumSize(QtCore.QSize(0, 200))
                card1_2.setMaximumSize(QtCore.QSize(500, 16777215))
                card1_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                card1_2.setAutoFillBackground(False)
                card1_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                card1_2.setFrameShadow(QtWidgets.QFrame.Raised)
                card1_2.setObjectName("card1_2")
                verticalLayout_7 = QtWidgets.QVBoxLayout(card1_2)
                verticalLayout_7.setContentsMargins(0, 0, 0, 0)
                verticalLayout_7.setObjectName("verticalLayout_7")
                card1Image_3 = QtWidgets.QWidget(card1_2)
                card1Image_3.setObjectName("card1Image_3")
                verticalLayout_9 = QtWidgets.QVBoxLayout(card1Image_3)
                verticalLayout_9.setContentsMargins(0, 0, 0, 0)
                verticalLayout_9.setObjectName("verticalLayout_9")
                card1ImageLabel_3 = QtWidgets.QLabel(card1Image_3)
                card1ImageLabel_3.setMinimumSize(QtCore.QSize(0, 100))
                font = QtGui.QFont()
                font.setPointSize(14)
                card1ImageLabel_3.setFont(font)
                card1ImageLabel_3.setAutoFillBackground(False)
                card1ImageLabel_3.setAlignment(QtCore.Qt.AlignCenter)
                card1ImageLabel_3.setObjectName("card1ImageLabel_3")
                card1ImageLabel_3.setText(_translate("MainWindow", project_name))
                verticalLayout_9.addWidget(card1ImageLabel_3)
                verticalLayout_7.addWidget(card1Image_3)
                card1DetailContainer_3 = QtWidgets.QWidget(card1_2)
                card1DetailContainer_3.setObjectName("card1DetailContainer_3")
                horizontalLayout_12 = QtWidgets.QHBoxLayout(card1DetailContainer_3)
                horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
                horizontalLayout_12.setObjectName("horizontalLayout_12")
                frame_4 = QtWidgets.QFrame(card1DetailContainer_3)
                frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
                frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
                frame_4.setObjectName("frame_4")
                verticalLayout_18 = QtWidgets.QVBoxLayout(frame_4)
                verticalLayout_18.setObjectName("verticalLayout_18")
                pushButton_4 = QtWidgets.QPushButton(frame_4)
                font = QtGui.QFont()
                font.setPointSize(11)
                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(":/icons/assets/image.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                pushButton_4.setFont(font)
                pushButton_4.setIcon(icon4)
                pushButton_4.setIconSize(QtCore.QSize(30, 30))
                pushButton_4.setObjectName("pushButton_4")
                pushButton_4.setText(_translate("MainWindow", no_of_images))
                verticalLayout_18.addWidget(pushButton_4)
                card1TotalImageLabel_3 = QtWidgets.QLabel(frame_4)
                font = QtGui.QFont()
                font.setPointSize(11)
                card1TotalImageLabel_3.setFont(font)
                card1TotalImageLabel_3.setAlignment(QtCore.Qt.AlignCenter)
                card1TotalImageLabel_3.setObjectName("card1TotalImageLabel_3")
                card1TotalImageLabel_3.setText(_translate("MainWindow", "Total Images"))
                verticalLayout_18.addWidget(card1TotalImageLabel_3)
                horizontalLayout_12.addWidget(frame_4)
                annotationDetail_3 = QtWidgets.QFrame(card1DetailContainer_3)
                annotationDetail_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                annotationDetail_3.setFrameShadow(QtWidgets.QFrame.Raised)
                annotationDetail_3.setObjectName("annotationDetail_3")
                verticalLayout_19 = QtWidgets.QVBoxLayout(annotationDetail_3)
                verticalLayout_19.setObjectName("verticalLayout_19")
                card1AnnotationShow_3 = QtWidgets.QPushButton(annotationDetail_3)
                font = QtGui.QFont()
                font.setPointSize(11)
                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap(":/icons/assets/check-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                card1AnnotationShow_3.setFont(font)
                card1AnnotationShow_3.setIcon(icon5)
                card1AnnotationShow_3.setIconSize(QtCore.QSize(30, 30))
                card1AnnotationShow_3.setObjectName("card1AnnotationShow_3")
                card1AnnotationShow_3.setText(_translate("MainWindow", annotations_count))
                verticalLayout_19.addWidget(card1AnnotationShow_3)
                card1AnnotationLabel_3 = QtWidgets.QLabel(annotationDetail_3)
                font = QtGui.QFont()
                font.setPointSize(11)
                card1AnnotationLabel_3.setFont(font)
                card1AnnotationLabel_3.setAlignment(QtCore.Qt.AlignCenter)
                card1AnnotationLabel_3.setObjectName("card1AnnotationLabel_3")
                card1AnnotationLabel_3.setText(_translate("MainWindow", "Total Annotations Done"))
                verticalLayout_19.addWidget(card1AnnotationLabel_3)
                horizontalLayout_12.addWidget(annotationDetail_3)
                verticalLayout_7.addWidget(card1DetailContainer_3)
                card1BottomContainer_3 = QtWidgets.QWidget(card1_2)
                card1BottomContainer_3.setMinimumSize(QtCore.QSize(0, 50))
                card1BottomContainer_3.setObjectName("card1BottomContainer_3")
                verticalLayout_20 = QtWidgets.QVBoxLayout(card1BottomContainer_3)
                verticalLayout_20.setObjectName("verticalLayout_20")
                projectDescription_3 = QtWidgets.QLabel(card1BottomContainer_3)
                font = QtGui.QFont()
                font.setPointSize(10)
                projectDescription_3.setFont(font)
                projectDescription_3.setObjectName("projectDescription_3")
                projectDescription_3.setText(_translate("MainWindow", "Description"))
                verticalLayout_20.addWidget(projectDescription_3)
                widget_6 = QtWidgets.QWidget(card1BottomContainer_3)
                widget_6.setMinimumSize(QtCore.QSize(0, 50))
                widget_6.setObjectName("widget_6")
                horizontalLayout_19 = QtWidgets.QHBoxLayout(widget_6)
                horizontalLayout_19.setObjectName("horizontalLayout_19")
                viewProjectBtn_3 = QtWidgets.QPushButton(widget_6)
                font = QtGui.QFont()
                font.setPointSize(-1)
                font.setBold(True)
                font.setWeight(75)
                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap(":/icons/assets/book-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                viewProjectBtn_3.setFont(font)
                viewProjectBtn_3.setText(_translate("MainWindow", "View Project"))
                viewProjectBtn_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                viewProjectBtn_3.setIcon(icon6)
                viewProjectBtn_3.setIconSize(QtCore.QSize(30, 30))
                viewProjectBtn_3.setStyleSheet(
                        "background-color: rgb(147, 208, 255);"
                        "border-radius: 5px;"
                        "padding: 10px;"
                        "font-size: 15px;"
                )
                viewProjectBtn_3.setObjectName(str(key))
                horizontalLayout_19.addWidget(viewProjectBtn_3, 0, QtCore.Qt.AlignHCenter)
                verticalLayout_20.addWidget(widget_6)
                verticalLayout_7.addWidget(card1BottomContainer_3)
                print(i,j)
                self.cardLayout.addWidget(card1_2,i,j, 1, 1)
                self.available_pushbuttons[key] = viewProjectBtn_3
                j += 1
                if j == 3:
                    j = 0
                    i += 1
                if i == 3:
                    break
            #print(self.availbale_pushbuttons)
            #print(dir(self.availbale_pushbuttons['1']))
            #self.availbale_pushbuttons['1'].clicked.connect(
            #    lambda: self.show_next_frame(self.availbale_pushbuttons['1'].objectName())
            #)
            print(self.available_pushbuttons)
            if len(self.available_pushbuttons) > 0:
                for key, value in self.available_pushbuttons.items():
                    value.clicked.connect(
                        lambda: self.show_next_frame(value.objectName())
                    )
            else:
                self.show_next_frame(None)

    def show_next_frame(self, project_id):
        self.stacked_widget.close()
        print("project id: ", project_id)
        project_id = int(project_id)
        main(self.app, self.access_token, project_id)

    def back_to_main(self):     
        self.stacked_widget.setCurrentIndex(0)
