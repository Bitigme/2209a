# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 13:25:17 2022

@author: dikol
"""
import json
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import time
import os
import socket
import base64
from PyQt5.QtMultimedia import *
import logging
from PIL import Image
import os
import PIL
import glob


class EdgeDetect(QWidget):

    def __init__(self):
        super(EdgeDetect, self).__init__()
        QMainWindow.__init__(self, None)

        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.mutex.lock()
        self.screen_width = int(QApplication.desktop().screenGeometry().width())
        self.screen_height = int(QApplication.desktop().screenGeometry().height())
        self.setAutoFillBackground(True)
        self.showFullScreen()
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(self.p)





        self.GeriButon = QPushButton()
        self.GeriButon.setIcon(QIcon('image/down-left1.png'))
        self.GeriButon.setIconSize(QSize(int(self.screen_width / 13.6), int(self.screen_height / 7.68)))

        self.GeriButon.setMaximumSize(int(self.screen_width / 10.88), int(self.screen_height / 6.144))
        self.GeriButon.setCursor(QCursor(Qt.PointingHandCursor))
        self.GeriButon.setStyleSheet("*{border: 4px solid '#9fb6cd';" +
                                     "border-top-left-radius: 10px; border-top-right-radius : 20px; border-bottom-left-radius : 50px; border-bottom-right-radius : 10px; " +
                                     "font-size: 30px;" +
                                     "color:'white'; " +
                                     "padding: 25px 0;" +
                                     "margin: 5px 3px;" +
                                     "background-color: '#e8e8e8';}" +
                                     "*:hover{background:'#9fb6cd';} ")

        #############################################
        self.lineEdit_Stili = """
                QLineEdit {
                        border: 2px solid #CCCCCC;
                        border-radius: 10px;
                        padding: 10px 20px 10px 20px;
                        font-family: "Segoe UI", sans-serif;
                        font-size: 22px;
                        font-weight: bold;
                        color: #333333;
                }

                QLineEdit:focus {
                        border: 2px solid #0078D7;
                        outline: none;
                }
                """
        self.label_Stili = """
                QLabel {
                    padding: 10px 20px 10px 20px;
                    font-family: "Segoe UI", sans-serif;
                    font-size: 22px;
                    font-weight: bold;
                    color: #333333;
                }

                QLabel:focus {
                    border: 2px solid #0078D7;
                    outline: none;
                }
        """
        #############################################


        self.Worker1 = Worker1(mutex=self.mutex, condition=self.condition)

        ############################################

        self.HB = QHBoxLayout()
        self.HB1 = QHBoxLayout()
        self.VB1 = QVBoxLayout()
        self.VB = QVBoxLayout()
        self.HB2 = QHBoxLayout()
        ############################################

        self.FeedLabel = QLabel()
        int(self.screen_width / 13.6), int(self.screen_height / 7.68)
        self.FeedLabel.setMaximumSize(int(self.screen_width / 2.22), int(self.screen_height / 1.30))

        self.FeedLabel.setFrameStyle(QFrame.Box)
        self.FeedLabel.setLineWidth(3)

        self.FeedLabel.setText("CAMERA Bağlantısı Bekleniyor...")
        self.FeedLabel.setFont(QFont('Times', int(self.screen_width / 136)))
        self.FeedLabel.setAlignment(Qt.AlignCenter)

        self.qline = QLineEdit()
        self.qline.setMaximumWidth(100)
        self.qline.setAlignment(Qt.AlignHCenter)
        self.qline.setStyleSheet(self.lineEdit_Stili)
        self.qlabel = QLabel("Statik Z (mm) ")
        self.qlabel.setStyleSheet(self.label_Stili)
        self.secim_buton = QPushButton("Seçimi Tamamla")
        self.secim_buton.setDisabled(False)
        self.secim_buton.clicked.connect(self.secim_f)
        self.secim_buton.setStyleSheet("*{border: 4px solid '#004C99';" +
                                      "border-radius: 20px 20px 50px 50px;" +
                                      "font-weight: bold;"+
                                      "font-size: {}px;".format(int(self.screen_width / 78.33)) +
                                      "color:'white'; " +
                                      "padding: 25px 0;" +
                                      "margin: 5px 3px;" +
                                      "background-color: rgb(128,128,128) ;}"+
                                       "*:hover{background:'#004C99';} " )
        self.slider_min_radius = QSlider(Qt.Horizontal)
        self.slider_min_radius.setMinimum(0)
        self.slider_min_radius.setMaximum(255)
        self.slider_min_radius.setValue(0)  # Or whatever default value you want
        self.slider_min_radius.valueChanged.connect(self.Worker1.set_min_radius)

        self.slider_max_radius = QSlider(Qt.Horizontal)
        self.slider_max_radius.setMinimum(0)
        self.slider_max_radius.setMaximum(255)
        self.slider_max_radius.setValue(0)  # Or whatever default value you want
        self.slider_max_radius.valueChanged.connect(self.Worker1.set_max_radius)

        self.slider_min_label = QLabel("Daire Min Yarıçap Ayarı")
        self.slider_min_label.setStyleSheet(self.label_Stili)

        self.slider_max_label = QLabel("Daire Max Yarıçap Ayarı")
        self.slider_max_label.setStyleSheet(self.label_Stili)

        self.HB.addWidget(self.FeedLabel)
        self.VB.addLayout(self.HB)

        self.HB1.addWidget(self.GeriButon)
        # self.HB1.addWidget(self.QLabel_Risk)
        self.HB2 = QHBoxLayout()


        self.HB2.addWidget(self.slider_min_label)
        self.HB2.addWidget(self.slider_min_radius)
        self.HB2.addWidget(self.slider_max_label)
        self.HB2.addWidget(self.slider_max_radius)

        self.hb2 = QHBoxLayout()
        self.hb2.addLayout(self.HB2)
        self.hb2.addWidget(self.qlabel)
        self.hb2.addWidget(self.qline)

        self.vbs = QVBoxLayout()
        self.vbs.addLayout(self.hb2)
        self.vbs.addWidget(self.secim_buton)

        self.HB1.addLayout(self.vbs)
        self.VB1.addLayout(self.HB1)
        self.VB.addLayout(self.VB1)


        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.GeriButon.clicked.connect(self.GeriDon)
        self.setLayout(self.VB)

    def ImageUpdateSlot(self, Image):
        self.mutex.lock()
        try:
            self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

        finally:
            self.mutex.unlock()
            self.condition.wakeAll()

    def GeriDon(self):

        QCloseEvent()
        self.Worker1.Durdur()
        self.close()
        return 0

        ### Bir önceki sınıfa ulaşmak için neler sayfalar arası haberleşmeye bak qtdeki gibi, bir önceki clası kapatıp açmak falan !

    def secim_f(self):
        self.qline.setDisabled(True)
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, mutex, condition):
        super().__init__()
        self.mutex = mutex
        self.condition = condition
        self.min_radius = 0
        self.max_radius = 0

    def set_min_radius(self, value):
        self.min_radius = value

    def set_max_radius(self, value):
        self.max_radius = value

    def run(self):
        QApplication.processEvents()
        self.cap = cv2.VideoCapture(0)
        self.Thread = True
        frame_counter = 0  # adding frame counter to skip some frames
        while self.Thread:
            QApplication.processEvents()
            ret, frame = self.cap.read()
            if ret:
                # processing every 10th frame only
                if frame_counter % 10 == 0:
                    screen_width = QApplication.desktop().screenGeometry().width()
                    screen_height = QApplication.desktop().screenGeometry().height()
                    frame = cv2.resize(frame, (int(screen_width / 2.22), int(screen_height / 1.30)))

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Skip frames when min_radius is not set yet
                    if self.min_radius != 0 and self.max_radius != 0:
                        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=30,
                                                   minRadius=self.min_radius, maxRadius=self.max_radius)

                        if circles is not None:
                            circles = np.uint16(np.around(circles))
                            for i in circles[0, :]:
                                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
                                cv2.putText(frame, f'x={i[0]}, y={i[1]}', (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                            (255, 255, 255), 2)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_with = frame.shape[0]
                    frame_height = frame.shape[1]

                    ConvertToQtFormat = QImage(frame.data, frame_height, frame_with, QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(frame_height, frame_with, Qt.KeepAspectRatio)

                    self.ImageUpdate.emit(Pic)
                    self.condition.wait(self.mutex)

                frame_counter += 1
        self.cap.release()

    def Durdur(self):
        self.Thread = False
        self.quit()
        self.exec_()







