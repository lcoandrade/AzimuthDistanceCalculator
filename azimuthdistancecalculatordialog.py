# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthDistanceCalculatorDialog
                                 A QGIS plugin
 Calculates azimuths and distances
                             -------------------
        begin                : 2014-09-24
        copyright            : (C) 2014 by Luiz Andrade
        email                : luiz.claudio@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

from PyQt4 import uic
from PyQt4.QtGui import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_azimuthdistancecalculator.ui'))

# Import specific modules
from AzimuthDistanceCalculator.kappaAndConvergence.calculateKappaAndConvergence import CalculateKappaAndConvergenceDialog
from AzimuthDistanceCalculator.azimuthsAndDistances.azimuthsAndDistances import AzimuthsAndDistancesDialog

class AzimuthDistanceCalculatorDialog(QDialog, FORM_CLASS):
    def __init__(self, iface):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        # Connecting SIGNAL/SLOTS for the Output button
        self.kappaAndConvergenceButton.clicked.connect(self.calculateKappa)

        # Connecting SIGNAL/SLOTS for the Output button
        self.azimuthsAndDistancesButton.clicked.connect(self.calculateAzimuths)

    def calculateKappa(self):
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            d = CalculateKappaAndConvergenceDialog(self.iface)
            d.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, open a layer and select a line or polygon feature."))

    def calculateAzimuths(self):
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            selectedFeatures = len(currentLayer.selectedFeatures())
            if selectedFeatures == 1: 
                selectedFeature = currentLayer.selectedFeatures()[0]
                d = AzimuthsAndDistancesDialog(self.iface, selectedFeature.geometry())
                d.exec_()
            else:
                QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("One and only one feature must be selected to perform the calculations."))
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, open a layer and select a line or polygon feature."))
