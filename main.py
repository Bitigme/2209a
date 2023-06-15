import PyQt5.QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import logging
from PIL import Image
import os
import PIL
import glob
from color_detection import ColorDetect
from edge_detection import EdgeDetect
import traceback

class ErrorApp:

    def raise_error(self):
        assert False

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    print("Hataya Git!")


class MainPage(QWidget):

    def __init__(self):
        super().__init__()
        #QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)

        self.screen_width = int(QApplication.desktop().screenGeometry().width())
        self.screen_height = int(QApplication.desktop().screenGeometry().height())



        grid = QGridLayout()
        self.setLayout(grid)

        logging.getLogger('PIL').setLevel(logging.WARNING)
        image = Image.open('image/subu_logo.png')

        resized_image = image.resize((int(self.screen_width / 4.53), int(self.screen_height / 2.56)), PIL.Image.ANTIALIAS)

        resized_image.save('a.png')

        image = Image.open('image/tübitak_logo.png')

        resized_image = image.resize((int(self.screen_width / 4.34), int(self.screen_height / 3.35)),PIL.Image.ANTIALIAS)

        resized_image.save('sn3.png')

        image = QPixmap('a.png')
        logo = QLabel()
        logo.setPixmap(image)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 5px")

        bosluk = QLabel()

        image2 = QPixmap('sn3.png')
        logo2 = QLabel()
        logo2.setPixmap(image2)
        logo2.setAlignment(Qt.AlignCenter)
        logo2.setMaximumSize(int(self.screen_width / 4.53), int(self.screen_height / 2.56))
        logo2.setStyleSheet("margin-top = 5px")
        names = ['Renk Tespiti', 'Daire Tespiti', 'Model Tespiti']
        positions = [(i, j) for i in range(2) for j in range(3)]
        self.A = []


        for position, name in zip(positions,names):
            button = QPushButton(name)
            self.A.append(button)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setStyleSheet("*{border: 4px solid '#004C99';" +
                                      "border-radius: 20px 20px 50px 50px;" +
                                      "font-weight: bold;"+
                                      "font-size: {}px;".format(int(self.screen_width / 38.33)) +
                                      "color:'white'; " +
                                      "padding: 25px 0;" +
                                      "margin: 5px 3px;" +
                                      "background-color: rgb(128,128,128) ;}"+
                                       "*:hover{background:'#004C99';} " )
            button.setFont(QFont("Times", 300))
            grid.addWidget(button,*position)
            print(*position)

        grid.addWidget(logo2)

        grid.addWidget(bosluk)

        grid.addWidget(logo)

        self.A[0].setMaximumSize(int(self.screen_width / 4.53), int(self.screen_height / 3.33))
        self.A[1].setMaximumSize(int(self.screen_width / 4.53), int(self.screen_height / 3.33))
        self.A[2].setMaximumSize(int(self.screen_width / 4.53), int(self.screen_height / 3.33))



        self.A[0].clicked.connect(self.Renk)
        self.A[1].clicked.connect(self.Sekil)
        self.A[2].clicked.connect(self.Model)


        #print(self.A[0].clicked.connect(lambda: self.whichbtn(self.A[0])))
        self.setLayout(grid)



    def Renk(self):
        self.renk = ColorDetect()
        self.renk.showFullScreen()
    def Sekil(self):
        self.edge = EdgeDetect()
        self.edge.showFullScreen()
    def Model(self):
        pass



app = QApplication(sys.argv)
main_page = MainPage()
main_page.showFullScreen()
sys.excepthook = excepthook
e = ErrorApp()
sys.exit(app.exec_())
