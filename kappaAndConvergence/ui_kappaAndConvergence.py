# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_kappaAndConvergence.ui'
#
# Created: Fri Sep 26 23:38:54 2014
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
        Dialog.resize(288, 400)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.longEdit = QtGui.QLineEdit(Dialog)
        self.longEdit.setObjectName(_fromUtf8("longEdit"))
        self.horizontalLayout.addWidget(self.longEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.latEdit = QtGui.QLineEdit(Dialog)
        self.latEdit.setObjectName(_fromUtf8("latEdit"))
        self.horizontalLayout_2.addWidget(self.latEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.calculateButton = QtGui.QPushButton(Dialog)
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.horizontalLayout_6.addWidget(self.calculateButton)
        self.clearButton = QtGui.QPushButton(Dialog)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_6.addWidget(self.clearButton)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "UTM Kappa factor and Convergence", None))
        self.label.setText(_translate("Dialog", "Longitude", None))
        self.longEdit.setToolTip(_translate("Dialog", "Use decimal degree values", None))
        self.label_2.setText(_translate("Dialog", "Latitude", None))
        self.latEdit.setToolTip(_translate("Dialog", "Use decimal degree values", None))
        self.calculateButton.setText(_translate("Dialog", "Calculate", None))
        self.clearButton.setText(_translate("Dialog", "Clear", None))

