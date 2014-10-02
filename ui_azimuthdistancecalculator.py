# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_azimuthdistancecalculator.ui'
#
# Created: Thu Oct 02 10:59:43 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AzimuthDistanceCalculator(object):
    def setupUi(self, AzimuthDistanceCalculator):
        AzimuthDistanceCalculator.setObjectName(_fromUtf8("AzimuthDistanceCalculator"))
        AzimuthDistanceCalculator.resize(416, 170)
        self.gridLayout = QtGui.QGridLayout(AzimuthDistanceCalculator)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.kappaAndConvergenceButton = QtGui.QPushButton(AzimuthDistanceCalculator)
        self.kappaAndConvergenceButton.setObjectName(_fromUtf8("kappaAndConvergenceButton"))
        self.gridLayout.addWidget(self.kappaAndConvergenceButton, 0, 0, 1, 2)
        self.azimuthsAndDistancesButton = QtGui.QPushButton(AzimuthDistanceCalculator)
        self.azimuthsAndDistancesButton.setObjectName(_fromUtf8("azimuthsAndDistancesButton"))
        self.gridLayout.addWidget(self.azimuthsAndDistancesButton, 1, 0, 1, 2)
        self.textEdit = QtGui.QTextEdit(AzimuthDistanceCalculator)
        self.textEdit.setEnabled(False)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AzimuthDistanceCalculator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(AzimuthDistanceCalculator)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AzimuthDistanceCalculator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AzimuthDistanceCalculator.reject)
        QtCore.QMetaObject.connectSlotsByName(AzimuthDistanceCalculator)

    def retranslateUi(self, AzimuthDistanceCalculator):
        AzimuthDistanceCalculator.setWindowTitle(QtGui.QApplication.translate("AzimuthDistanceCalculator", "AzimuthDistanceCalculator", None, QtGui.QApplication.UnicodeUTF8))
        self.kappaAndConvergenceButton.setText(QtGui.QApplication.translate("AzimuthDistanceCalculator", "Calculate Kappa And Convergence", None, QtGui.QApplication.UnicodeUTF8))
        self.azimuthsAndDistancesButton.setToolTip(QtGui.QApplication.translate("AzimuthDistanceCalculator", "Generates a CSV with azimuths and distances for the selected feature", None, QtGui.QApplication.UnicodeUTF8))
        self.azimuthsAndDistancesButton.setText(QtGui.QApplication.translate("AzimuthDistanceCalculator", "Calculate Azimuths and Distances", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("AzimuthDistanceCalculator", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; color:#ff0000;\">All files generated are made according to the brazilian laws. Feel free to check the code and make the documents in your language.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

