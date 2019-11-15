# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'draft.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_image = QtWidgets.QFrame(self.centralwidget)
        self.input_image.setGeometry(QtCore.QRect(40, 130, 500, 500))
        self.input_image.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.input_image.setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_image.setObjectName("input_image")
        self.process = QtWidgets.QPushButton(self.centralwidget)
        self.process.setGeometry(QtCore.QRect(585, 330, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.process.setFont(font)
        self.process.setObjectName("process")
        self.select_picture = QtWidgets.QPushButton(self.centralwidget)
        self.select_picture.setEnabled(True)
        self.select_picture.setGeometry(QtCore.QRect(110, 10, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.select_picture.setFont(font)
        self.select_picture.setObjectName("select_picture")
        self.revert = QtWidgets.QPushButton(self.centralwidget)
        self.revert.setEnabled(True)
        self.revert.setGeometry(QtCore.QRect(160, 650, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.revert.setFont(font)
        self.revert.setObjectName("revert")
        self.select_pencil = QtWidgets.QPushButton(self.centralwidget)
        self.select_pencil.setGeometry(QtCore.QRect(160, 100, 111, 27))
        self.select_pencil.setObjectName("select_pencil")
        self.select_eraser = QtWidgets.QPushButton(self.centralwidget)
        self.select_eraser.setGeometry(QtCore.QRect(280, 100, 111, 27))
        self.select_eraser.setObjectName("select_eraser")
        self.last_steps = QtWidgets.QComboBox(self.centralwidget)
        self.last_steps.setGeometry(QtCore.QRect(400, 100, 141, 27))
        self.last_steps.setStatusTip("")
        self.last_steps.setWhatsThis("")
        self.last_steps.setCurrentText("")
        self.last_steps.setMaxVisibleItems(10)
        self.last_steps.setObjectName("last_steps")
        self.tool_pt_size = QtWidgets.QComboBox(self.centralwidget)
        self.tool_pt_size.setEnabled(True)
        self.tool_pt_size.setGeometry(QtCore.QRect(40, 100, 111, 27))
        self.tool_pt_size.setStatusTip("")
        self.tool_pt_size.setCurrentText("")
        self.tool_pt_size.setMaxVisibleItems(10)
        self.tool_pt_size.setObjectName("tool_pt_size")
        self.output_image = QtWidgets.QFrame(self.centralwidget)
        self.output_image.setGeometry(QtCore.QRect(760, 130, 500, 500))
        self.output_image.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.output_image.setFrameShadow(QtWidgets.QFrame.Raised)
        self.output_image.setObjectName("output_image")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setEnabled(True)
        self.save.setGeometry(QtCore.QRect(760, 50, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.save.setFont(font)
        self.save.setObjectName("save")
        self.show_image_full_size = QtWidgets.QPushButton(self.centralwidget)
        self.show_image_full_size.setGeometry(QtCore.QRect(1150, 50, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.show_image_full_size.setFont(font)
        self.show_image_full_size.setObjectName("show_image_full_size")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.last_steps.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DeFINe – Deep Facial Inpainting Network"))
        MainWindow.setToolTip(_translate("MainWindow", "Utilize \'Inpainting\' to fix your pictures."))
        self.process.setText(_translate("MainWindow", "GO"))
        self.select_picture.setText(_translate("MainWindow", "Select Picture"))
        self.revert.setText(_translate("MainWindow", "Revert"))
        self.select_pencil.setText(_translate("MainWindow", "Pencil"))
        self.select_eraser.setText(_translate("MainWindow", "Eraser"))
        self.last_steps.setToolTip(_translate("MainWindow", "Revert to a previous version"))
        self.last_steps.setAccessibleName(_translate("MainWindow", "Last Steps"))
        self.tool_pt_size.setToolTip(_translate("MainWindow", "Select the tool pt size."))
        self.tool_pt_size.setAccessibleName(_translate("MainWindow", "Tool pt size"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.show_image_full_size.setText(_translate("MainWindow", "Full Size"))

