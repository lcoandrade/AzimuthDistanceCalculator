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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui_azimuthdistancecalculator import Ui_AzimuthDistanceCalculator

import os.path, sys
# Import specific modules
# Set up current path, so that we know where to look for modules
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/kappaAndConvergence'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/azimuthsAndDistances'))
import calculateKappaAndConvergence
import azimuthsAndDistances
################################################################

class AzimuthDistanceCalculatorDialog(QDialog, Ui_AzimuthDistanceCalculator):
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
        QObject.connect(self.kappaAndConvergenceButton, SIGNAL("clicked()"), self.calculateKappa)

        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.azimuthsAndDistancesButton, SIGNAL("clicked()"), self.calculateAzimuths)

    def calculateKappa(self):
        d = calculateKappaAndConvergence.CalculateKappaAndConvergenceDialog(self.iface)
        d.exec_()

    def calculateAzimuths(self):
        currentLayer = self.iface.mapCanvas().currentLayer()
        selectedFeatures = len(currentLayer.selectedFeatures())
        if selectedFeatures == 1: 
            selectedFeature = currentLayer.selectedFeatures()[0]
            d = azimuthsAndDistances.AzimuthsAndDistancesDialog(self.iface, selectedFeature.geometry())
            d.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "One and only one feature must be selected to perform the calculations.")

