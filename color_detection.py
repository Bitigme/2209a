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


class ColorDetect(QWidget):

    def __init__(self):
        super(ColorDetect, self).__init__()

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
        self.FeedLabel1 = QLabel()
        int(self.screen_width / 13.6), int(self.screen_height / 7.68)
        self.FeedLabel.setMaximumSize(int(self.screen_width / 2.22), int(self.screen_height / 1.30))
        self.FeedLabel1.setMaximumSize(int(self.screen_width / 2.22), int(self.screen_height / 1.30))

        self.FeedLabel.setFrameStyle(QFrame.Box)
        self.FeedLabel1.setFrameStyle(QFrame.Box)
        self.FeedLabel1.setLineWidth(3)
        self.FeedLabel.setLineWidth(3)

        self.FeedLabel.setText("CAMERA1 Bağlantısı Bekleniyor...")
        self.FeedLabel.setFont(QFont('Times', int(self.screen_width / 136)))

        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(255)
        self.slider1.valueChanged.connect(self.update_slider1_value)

        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(255)
        self.slider2.valueChanged.connect(self.update_slider2_value)

        self.slider3 = QSlider(Qt.Horizontal, self)
        self.slider3.setMinimum(0)
        self.slider3.setMaximum(255)
        self.slider3.valueChanged.connect(self.update_slider3_value)

        self.slider1_label = QLabel('0', self)
        self.slider2_label = QLabel('0', self)
        self.slider3_label = QLabel('0', self)

        self.slider1_layout = QHBoxLayout()
        self.slider1_layout.addWidget(self.slider1)
        self.slider1_layout.addWidget(self.slider1_label)

        self.slider2_layout = QHBoxLayout()
        self.slider2_layout.addWidget(self.slider2)
        self.slider2_layout.addWidget(self.slider2_label)

        self.slider3_layout = QHBoxLayout()
        self.slider3_layout.addWidget(self.slider3)
        self.slider3_layout.addWidget(self.slider3_label)

        self.qline = QLineEdit()
        self.qline.setMaximumWidth(100)
        self.qline.setAlignment(Qt.AlignHCenter)
        self.qline.setStyleSheet(self.lineEdit_Stili)
        self.qlabel = QLabel("Statik Z (mm) ")
        self.qlabel.setStyleSheet(self.label_Stili)
        self.secim_buton = QPushButton("Seçimi Tamamla")
        self.secim_buton.setStyleSheet("*{border: 4px solid '#004C99';" +
                                      "border-radius: 20px 20px 50px 50px;" +
                                      "font-weight: bold;"+
                                      "font-size: {}px;".format(int(self.screen_width / 78.33)) +
                                      "color:'white'; " +
                                      "padding: 25px 0;" +
                                      "margin: 5px 3px;" +
                                      "background-color: rgb(128,128,128) ;}"+
                                       "*:hover{background:'#004C99';} " )

        self.HB.addWidget(self.FeedLabel)
        self.HB.addWidget(self.FeedLabel1)
        self.VB.addLayout(self.HB)

        self.HB1.addWidget(self.GeriButon)
        # self.HB1.addWidget(self.QLabel_Risk)
        self.VB2 = QVBoxLayout()
        self.VB2.addLayout(self.slider1_layout)
        self.VB2.addLayout(self.slider2_layout)
        self.VB2.addLayout(self.slider3_layout)

        self.hb2 = QHBoxLayout()
        self.hb2.addLayout(self.VB2)
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

    def ImageUpdateSlot(self, Image,Image2):
        self.mutex.lock()

        try:
            self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
            self.FeedLabel1.setPixmap(QPixmap.fromImage(Image2))

        finally:
            self.mutex.unlock()
            self.condition.wakeAll()

    def GeriDon(self):

        QCloseEvent()
        self.Worker1.Durdur()
        self.close()
        return 0

        ### Bir önceki sınıfa ulaşmak için neler sayfalar arası haberleşmeye bak qtdeki gibi, bir önceki clası kapatıp açmak falan !

    def update_slider1_value(self, value):
        self.slider1_label.setText(str(value))
        self.Worker1.set_threshold(0, value)

    def update_slider2_value(self, value):
        self.slider2_label.setText(str(value))
        self.Worker1.set_threshold(1, value)

    def update_slider3_value(self, value):
        self.slider3_label.setText(str(value))
        self.Worker1.set_threshold(2, value)


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage,QImage)

    def __init__(self, mutex, condition):
        super().__init__()
        self.mutex = mutex
        self.condition = condition
        self.lower_color = np.array([0, 0, 0])
        self.upper_color = np.array([0, 0, 0])

    def run(self):

        self.cap = cv2.VideoCapture(0)
        self.Thread = True

        while self.Thread:
            ret, frame = self.cap.read()
            if ret:
                screen_width = QApplication.desktop().screenGeometry().width()
                screen_height = QApplication.desktop().screenGeometry().height()
                frame = cv2.resize(frame, (int(screen_width / 2.22), int(screen_height / 1.30)))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_with = frame.shape[0]
                frame_height = frame.shape[1]
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
                res = cv2.bitwise_and(frame, frame, mask=mask)

                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                min_area = 200  # Minimum contour area to consider
                max_area = 2000  # Maximum contour area to consider

                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 400:
                        # Compute the bounding rectangle
                        x, y, w, h = cv2.boundingRect(contour)

                        # Draw the bounding rectangle
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                        # Calculate moments for each contour
                        M = cv2.moments(contour)

                        # Calculate x,y coordinate of center
                        if M["m00"] != 0:
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                        else:
                            cX, cY = 0, 0

                        # Draw the center of the shape on the image
                        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

                        # Write coordinates on the frame
                        cv2.putText(frame, f"X: {cX}, Y: {cY}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

                        # Draw contours
                        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)


                ConvertToQtFormat = QImage(frame.data, frame_height, frame_with, QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(frame_height, frame_with, Qt.KeepAspectRatio)

                ConvertToQtFormat2 = QImage(res.data, frame_height, frame_with, QImage.Format_RGB888)
                Pic2 = ConvertToQtFormat2.scaled(frame_height, frame_with, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(Pic,Pic2)
                self.condition.wait(self.mutex)
        self.cap.release()

    def Durdur(self):
        self.Thread = False
        self.quit()
        self.exec_()

    def set_threshold(self, index, value):
        if index == 0:
            self.lower_color[0] = value
        elif index == 1:
            self.lower_color[1] = value
        elif index == 2:
            self.lower_color[2] = value

        self.upper_color = np.array([self.lower_color[0] + 20, 255, 255])




