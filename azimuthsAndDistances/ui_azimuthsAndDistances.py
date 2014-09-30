# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_azimuthsAndDistances.ui'
#
# Created: Tue Sep 30 20:02:45 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(723, 338)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.calculateButton = QtGui.QPushButton(Dialog)
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.horizontalLayout_2.addWidget(self.calculateButton)
        self.clearButton = QtGui.QPushButton(Dialog)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_2.addWidget(self.clearButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.saveFilesButton = QtGui.QPushButton(Dialog)
        self.saveFilesButton.setObjectName(_fromUtf8("saveFilesButton"))
        self.gridLayout.addWidget(self.saveFilesButton, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Azimuths and Distances", None))
        self.label.setText(_translate("Dialog", "Geometry Description", None))
        self.label_2.setText(_translate("Dialog", "Inform the Meridian Convergence:", None))
        self.lineEdit.setToolTip(_translate("Dialog", "Use decimal degrees", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Vertex", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "E", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "N", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Side", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Planar Azimuth", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Real Azimuth", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Distance", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "Confronting", None))
        self.calculateButton.setText(_translate("Dialog", "Calculate", None))
        self.clearButton.setText(_translate("Dialog", "Clear", None))
        self.saveFilesButton.setText(_translate("Dialog", "Save Files", None))

