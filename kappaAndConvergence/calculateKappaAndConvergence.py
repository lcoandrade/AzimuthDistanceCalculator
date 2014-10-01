# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Calculator
# Purpose:
#
# Author:      Luiz Andrade - luiz.claudio@dsg.eb.mil.br
#
# Created:     24/09/2014
# Copyright:   (c) luiz 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import math

from ui_kappaAndConvergence import Ui_Dialog

class CalculateKappaAndConvergenceDialog( QDialog, Ui_Dialog ):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.calculateButton, SIGNAL("clicked()"), self.fillTextEdit)
        
        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.clearButton, SIGNAL("clicked()"), self.clearTextEdit)
        
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
        self.textEdit.append("UTM Zone = "+str(utmZone)+"\n")
        self.textEdit.append("Central Meridian = "+str(centralMeridian)+"\n")
        self.textEdit.append("Kappa = "+str(reducedKappa)+"\n")
        self.textEdit.append("Convergence DMS = "+convergence+"\n")
        self.textEdit.append("Convergence Decimal Degrees = "+str(c)+"\n")
        
    def clearTextEdit(self):
        self.textEdit.clear()