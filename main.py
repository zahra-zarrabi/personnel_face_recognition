# This Python file uses the following encoding: utf-8
import sys

import cv2
from PySide6.QtWidgets import *

from PySide6.QtUiTools import QUiLoader
from PySide6 import QtGui
from functools import partial
from PySide6 import QtCore,Qt
from PySide6.QtGui import QPixmap,QImage
from functools import partial
from datetime import datetime

from sql import Database


def ConvertCvimage2Qtimage(cv_image):
    # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    height, width, channel = cv_image.shape
    # bytesperline=3*width
    qimg = QImage(cv_image.data, width, height, QImage.Format_BGR888)
    return QPixmap.fromImage(qimg)

class MainWindow:
    def __init__(self):
        super(MainWindow, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('dialog.ui')
        self.ui.show()

        self.ui.btn_personnel.clicked.connect(self.read_personnel)
        self.ui.btn_add.clicked.connect(self.add_window)

    def add_window(self):
        # self.hide()
        # creat a new window
        self.win = QWidget()
        self.win.resize(200, 150)
        self.win.setWindowTitle('Add new personnel')

        self.grid = QGridLayout()
        self.win.setLayout(self.grid)

        # label
        self.lbl = QLabel()
        self.lbl.setText("مشخصات فردی ")
        self.lbl.setFont(QtGui.QFont("Ubuntu", 30))
        self.grid.addWidget(self.lbl, 0, 3)

        self.label_name = QLabel()
        self.label_name.setText("name :")
        self.grid.addWidget(self.label_name,1, 0)

        self.label_family = QLabel()
        self.label_family.setText("family :")
        self.grid.addWidget(self.label_family, 2, 0)

        self.label_code = QLabel()
        self.label_code.setText("national code :")
        self.grid.addWidget(self.label_code, 3, 0)

        self.label_birth = QLabel()
        self.label_birth.setText("date of birth :")
        self.grid.addWidget(self.label_birth, 4, 0)

        self.label_Image = QLabel()
        self.label_Image.setText("image :")
        self.grid.addWidget(self.label_Image, 5, 0)

        # text
        self.text_name = QLineEdit()
        self.text_name.setPlaceholderText("نام")
        self.grid.addWidget(self.text_name, 1, 1)

        self.text_family = QLineEdit()
        self.text_family.setPlaceholderText("نام خانوادگی")
        self.grid.addWidget(self.text_family, 2, 1)

        self.text_code = QLineEdit()
        self.text_code.setPlaceholderText("کد ملی")
        self.grid.addWidget(self.text_code, 3, 1)

        self.text_birth = QLineEdit()
        self.text_birth.setPlaceholderText("تاریخ تولد")
        self.grid.addWidget(self.text_birth, 4, 1)

        self.btn_img = QPushButton()
        self.btn_img.setText("گرفتن عکس")
        # self.btn_img.setMaximumSize(35,25)
        self.grid.addWidget(self.btn_img,5, 1)
        self.btn_img.clicked.connect(partial(self.my_webcan,[self.text_family, self.grid]))

        self.label_Img = QLabel()
        self.label_Img.setMaximumSize(200, 200)
        # self.label_Img.setText("image :")
        self.grid.addWidget(self.label_Img, 6, 1)
        print(self.label_Img.text())

        self.btn_save = QPushButton()
        self.btn_save.setText("save")
        self.grid.addWidget(self.btn_save, 6, 2)
        self.btn_save.clicked.connect(partial(self.addnewpersonnel,self.text_name,self.text_family,self.text_code, self.text_birth, self.label_Img))

        self.win.show()

        # loader = QUiLoader()
        # self.ui = loader.load('add_person.ui')
        # self.ui.show()


    def my_webcan(self,x):
        family, grid = x[0].text(), x[1]
        self.win.grid=grid
        # self.label_Img = QLabel()
        # self.label_Img.setMaximumSize(200,200)
        # self.label_Img.setText("image :")
        # self.win.grid.addWidget(self.label_Img,6,1)


        my_video=cv2.VideoCapture(0)
        while True:
            ret, frame=my_video.read()
            if not ret:
                break
            cv2.imshow('out',frame)
            # cv2.waitKey(1)
            if cv2.waitKey(1)==ord('s'):
                cv2.imwrite(f'{family}.jpg',frame)
                break

        qimg= ConvertCvimage2Qtimage(frame)

        # pix=QtGui.QPixmap.fromImage(qimg)
        self.pix_img=QtGui.QPixmap(qimg)

        # QtGui.QPixmap.resize(30)

        self.label_Img.setPixmap(self.pix_img.scaled(150,150))


    def read_personnel(self):
        personnel = Database.my_select()
        print(personnel)
        self.row = len(personnel)
        for i,person in enumerate(personnel):
            label_code = QLabel()
            label_code.setText(str(person[0]))
            self.ui.gridLayout_staff.addWidget(label_code, i, 0)

            label_1 = QLabel()
            label_1.setText(person[1] + " " + person[2])
            self.ui.gridLayout_staff.addWidget(label_1,i,1)

            label_birth = QLabel()
            label_birth.setText(str(person[3]))
            self.ui.gridLayout_staff.addWidget(label_birth, i, 2)

            label_image = QLabel()
            label_image.setText(person[4])
            self.ui.gridLayout_staff.addWidget(label_image, i, 3)

            btn_edit=QPushButton()
            btn_edit.setIcon(QtGui.QIcon('edit-user.png'))
            btn_edit.clicked.connect(partial(self.editpersonnel))
            self.ui.gridLayout_staff.addWidget(btn_edit,i,5)

            btn_delet=QPushButton()
            btn_delet.setIcon(QtGui.QIcon('images.jpeg'))
            btn_delet.clicked.connect(partial(self.removepersonnel,btn_delet,person[0],label_image,label_1,label_birth,label_code,btn_edit))
            self.ui.gridLayout_staff.addWidget(btn_delet,i,4)

    def removepersonnel(self,btn_delet,code,label_image,label_1,label_birth,label_code,btn_edit):
        response=Database.my_delete(code)
        if response:
            btn_delet.hide()
            btn_edit.hide()
            label_code.hide()
            label_image.hide()
            label_1.hide()
            label_birth.hide()
            msg_box = QMessageBox()
            msg_box.setText('Deleted.')
            msg_box.exec_()

    def addnewpersonnel(self,name1,family1,code1,birth1,image1):
        name = name1.text()
        family = family1.text()
        code = code1.text()
        birth = birth1.text()
        image = image1.text()
        print(image)

        # personnel = Database.my_select()

        if code != "" and family != "":
            response=Database.my_insert(code,name,family,birth,image)
            print(response)
            if response==True:
                label_code = QLabel()
                label_code.setText(code)
                # label.setStyleSheet('color:red')
                self.ui.gridLayout_staff.addWidget(label_code, self.row, 0)

                label = QLabel()
                label.setText(name + " " + family)
                # label.setStyleSheet('color:red')
                self.ui.gridLayout_staff.addWidget(label, self.row, 1)

                label_birth = QLabel()
                label_birth.setText(birth)
                # label_birth.setStyleSheet('color:red')
                self.ui.gridLayout_staff.addWidget(label_birth, self.row, 2)

                label_image = QLabel()
                label_image.setText(image)
                # label_birth.setStyleSheet('color:red')
                self.ui.gridLayout_staff.addWidget(label_image, self.row, 3)

                btn_delet = QPushButton()
                btn_delet.setIcon(QtGui.QIcon('images.jpeg'))
                btn_delet.clicked.connect(partial(self.removepersonnel,btn_delet,code,label,label_birth,label_code))
                self.ui.gridLayout_staff.addWidget(btn_delet, self.row, 4)

                btn_edit = QPushButton()
                btn_edit.setIcon(QtGui.QIcon('edit-user.png'))
                btn_edit.clicked.connect(partial(self.editpersonnel))
                self.ui.gridLayout_staff.addWidget(btn_edit, self.row, 5)

                self.row += 1

                # self.ui.lineEdit_name.setText("")
                # self.ui.lineEdit_message.setText("")

                msg_box = QMessageBox()
                msg_box.setText('your message sent successfully!')
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setText('Database Error.')
                msg_box.exec_()

            name1.setText("")
            family1.setText("")
            code1.setText("")
            birth1.setText("")
            image1.setText("")

        else:
            msg_box = QMessageBox()
            msg_box.setText('Error: fields are empty!')
            msg_box.exec_()

    def editpersonnel(self):
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # window.show()
    sys.exit(app.exec_())
