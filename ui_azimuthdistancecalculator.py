# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_azimuthdistancecalculator.ui'
#
# Created: Fri Sep 26 23:38:03 2014
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

class Ui_AzimuthDistanceCalculator(object):
    def setupUi(self, AzimuthDistanceCalculator):
        AzimuthDistanceCalculator.setObjectName(_fromUtf8("AzimuthDistanceCalculator"))
        AzimuthDistanceCalculator.resize(362, 105)
        self.gridLayout = QtGui.QGridLayout(AzimuthDistanceCalculator)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.kappaAndConvergenceButton = QtGui.QPushButton(AzimuthDistanceCalculator)
        self.kappaAndConvergenceButton.setObjectName(_fromUtf8("kappaAndConvergenceButton"))
        self.gridLayout.addWidget(self.kappaAndConvergenceButton, 0, 0, 1, 1)
        self.azimuthsAndDistancesButton = QtGui.QPushButton(AzimuthDistanceCalculator)
        self.azimuthsAndDistancesButton.setObjectName(_fromUtf8("azimuthsAndDistancesButton"))
        self.gridLayout.addWidget(self.azimuthsAndDistancesButton, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AzimuthDistanceCalculator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(AzimuthDistanceCalculator)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AzimuthDistanceCalculator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AzimuthDistanceCalculator.reject)
        QtCore.QMetaObject.connectSlotsByName(AzimuthDistanceCalculator)

    def retranslateUi(self, AzimuthDistanceCalculator):
        AzimuthDistanceCalculator.setWindowTitle(_translate("AzimuthDistanceCalculator", "AzimuthDistanceCalculator", None))
        self.kappaAndConvergenceButton.setText(_translate("AzimuthDistanceCalculator", "Calculate Kappa And Convergence", None))
        self.azimuthsAndDistancesButton.setToolTip(_translate("AzimuthDistanceCalculator", "Generates a CSV with azimuths and distances for the selected feature", None))
        self.azimuthsAndDistancesButton.setText(_translate("AzimuthDistanceCalculator", "Calculate Azimuths and Distances", None))

