# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthDistanceCalculator
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
from qgis.core import *

import math

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_kappaAndConvergence.ui'))

class CalculateKappaAndConvergenceDialog(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        # Connecting SIGNAL/SLOTS for the Output button
        self.calculateButton.clicked.connect(self.fillTextEdit)

        # Connecting SIGNAL/SLOTS for the Output button
        self.clearButton.clicked.connect(self.clearTextEdit)

        self.latEdit.setInputMask("#00.00000")
        self.longEdit.setInputMask("#000.00000")
    
    def calculateKappa(self):
        """Calculates the linear deformation factor (Kappa) for UTM projections
        """
        kappaZero = 0.9996
        latitude = float(self.latEdit.text())
        longitude = float(self.longEdit.text())
        centralMeridian = int(abs(longitude)/6)*6 + 3
        if longitude < 0:
            centralMeridian = centralMeridian*(-1)

        
        b = math.cos(math.radians(latitude))*math.sin(math.radians(longitude - centralMeridian))
        
        k = kappaZero/math.sqrt(1 - b*b)
        
        return k
    
    def calculateConvergence(self, a, b):
        """Calculates the meridian convergence
        """
        latitude = float(self.latEdit.text())
        longitude = float(self.longEdit.text())
        centralMeridian = int(abs(longitude)/6)*6 + 3
        if longitude < 0:
            centralMeridian = centralMeridian*(-1)
        
        deltaLong = abs( centralMeridian - longitude )
        
        p = 0.0001*( deltaLong*3600 )
        
        xii = math.sin(math.radians(latitude))*math.pow(10, 4)
        
        e2 = math.sqrt(a*a - b*b)/b
        
        c5 = math.pow(math.sin(math.radians(1/3600)), 4)*math.sin(math.radians(latitude))*math.pow(math.cos(math.radians(latitude)), 4)*(2 - math.pow(math.tan(math.radians(latitude)), 2))*math.pow(10, 20)/15
        
        xiii = math.pow(math.sin(math.radians(1/3600)), 2)*math.sin(math.radians(latitude))*math.pow(math.cos(math.radians(latitude)), 2)*(1 + 3*e2*e2*math.pow(math.cos(math.radians(latitude)), 2) + 2*math.pow(e2, 4)*math.pow(math.cos(math.radians(latitude)), 4))*math.pow(10, 12)/3
        
        cSeconds = xii*p + xiii*math.pow(p, 3) + c5*math.pow(p, 5)
        
        c = cSeconds/3600
        
        return c
        
    def getSemiMajorAndSemiMinorAxis(self):
        """Obtains the semi major axis and semi minor axis from the used ellipsoid
        """
        currentLayer = self.iface.mapCanvas().currentLayer()
        distanceArea = QgsDistanceArea()
        distanceArea.setEllipsoid(currentLayer.crs().ellipsoidAcronym())
        a = distanceArea.ellipsoidSemiMajor()
        b = distanceArea.ellipsoidSemiMinor()
        
        return (a,b)
    
    def getPlanarCoordinates(self):
        """Transform the geographic coordinates to projected coordinates
        """
        latitude = float(self.latEdit.text())
        longitude = float(self.longEdit.text())
        
        crsDest = self.iface.mapCanvas().currentLayer().crs()
        crsSrc = QgsCoordinateReferenceSystem(crsDest.geographicCRSAuthId())
        
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        
        utmPoint = coordinateTransformer.transform(QgsPoint(longitude, latitude))
        
        return utmPoint
        
    def fillTextEdit(self):
        """Fills the text area with the calculated information
        """
        self.textEdit.clear()
        
        latitude = float(self.latEdit.text())
        longitude = float(self.longEdit.text())
        centralMeridian = int(abs(longitude)/6)*6 + 3
        if longitude < 0:
            centralMeridian = centralMeridian*(-1)
        utmZone = int(centralMeridian/6) + 31
        
        ab = self.getSemiMajorAndSemiMinorAxis()
        
        reducedKappa = self.calculateKappa()
        c = self.calculateConvergence(ab[0], ab[1])
        
        convergenceGrau = int(c)
        convergenceMinuto = abs(int(60*(c-int(c))))
        convergenceSegundo = abs((c-convergenceGrau-convergenceMinuto/60)*60)
        convergence = str(convergenceGrau) + u"\u00b0" + str(convergenceMinuto).zfill(2) + "'" + "%0.2f"%(convergenceSegundo) + "''"
        
        utmPoint = self.getPlanarCoordinates()
        
        self.textEdit.append("N = "+str(utmPoint.y())+"\n")
        self.textEdit.append("E = "+str(utmPoint.x())+"\n")
        self.textEdit.append("Long = "+str(longitude)+"\n")
        self.textEdit.append("Lat = "+str(latitude)+"\n")
        self.textEdit.append(self.tr("UTM Zone = ")+str(utmZone)+"\n")
        self.textEdit.append(self.tr("Central Meridian = ")+str(centralMeridian)+"\n")
        self.textEdit.append(self.tr("Kappa = ")+str(reducedKappa)+"\n")
        self.textEdit.append(self.tr("Convergence DMS = ")+convergence+"\n")
        self.textEdit.append(self.tr("Convergence Decimal Degrees = ")+str(c)+"\n")
        
    def clearTextEdit(self):
        self.textEdit.clear()