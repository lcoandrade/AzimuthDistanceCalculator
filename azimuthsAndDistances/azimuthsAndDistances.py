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

from ui_azimuthsAndDistances import Ui_Dialog

import memorialGenerator

class AzimuthsAndDistancesDialog( QDialog, Ui_Dialog ):
    """Class that calculates azimuths and distances among vertexes in a linestring.
    """
    def __init__(self, iface, geometry):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )

        self.geom = geometry
        self.iface = iface
        self.points = None
        self.distancesAndAzimuths = None
        self.area = self.geom.area()
        
        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.calculateButton, SIGNAL("clicked()"), self.fillTextEdit)
        
        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.clearButton, SIGNAL("clicked()"), self.clearTextEdit)

        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.saveFilesButton, SIGNAL("clicked()"), self.saveFiles)
        
        self.lineEdit.setInputMask("#00.00000")
        
    def saveFiles(self):
        if (not self.distancesAndAzimuths) or (not self.points):
            QMessageBox.information(self.iface.mainWindow(), "Warning!", "Click on calculate button first to generate the needed data.")
        else:
            confrontingList = list()
            for i in xrange(self.tableWidget.rowCount()):
                item = self.tableWidget.item(i, 7)
                confrontingList.append(item.text())
                
            d = memorialGenerator.MemorialGenerator(self.lineEdit.text(), self.distancesAndAzimuths, self.points, confrontingList, self.area, self.perimeter)
            d.exec_()
        
    def isValidType(self):
        """Verifies the geometry type.
        """
        if self.geom.isMultipart():
            QMessageBox.information(self.iface.mainWindow(), "Warning!", "The limit of a patrimonial area must be a single part geometry.")
            return False

        if self.geom.type() == QGis.Line:
            self.points = self.geom.asPolyline()
            return True
        elif self.geom.type() == QGis.Polygon:
            self.points = self.geom.asPolygon()[0]
            return True            
        else:
            QMessageBox.information(self.iface.mainWindow(), "Warning!", "The selected geometry should be a Line or a Polygon.")
            return False
            
    def calculate(self):
        """Constructs a list with distances and azimuths.
        """
        self.perimeter = 0
        self.distancesAndAzimuths = list()
        for i in xrange(0,len(self.points)-1):
            before = self.points[i]
            after = self.points[i+1]
            distance = math.sqrt(before.sqrDist(after))
            azimuth = before.azimuth(after)
            self.distancesAndAzimuths.append((distance, azimuth))
            self.perimeter += distance
            
        return self.distancesAndAzimuths
            
    def fillTextEdit(self):
        """Makes the CSV.
        """
        distancesAndAzimuths = list()
        isValid = self.isValidType()
        if isValid:
            distancesAndAzimuths = self.calculate()
        try:
            convergence = float(self.lineEdit.text())
        except ValueError:
            QMessageBox.information(self.iface.mainWindow(), "Warning!", "Please, insert the meridian convergence.")
            return 
            
        isClosed = False
        if self.points[0] == self.points[len(self.points) - 1]:
            isClosed = True
        
        self.tableWidget.setRowCount(len(distancesAndAzimuths))

        for i in xrange(0,len(distancesAndAzimuths)):            
            azimuth = self.dd2dms(distancesAndAzimuths[i][1])
            realAzimuth = self.dd2dms(distancesAndAzimuths[i][1] + convergence)
            
            itemVertex = QTableWidgetItem("Pt"+str(i))
            self.tableWidget.setItem(i,0,itemVertex)
            itemE = QTableWidgetItem(str(self.points[i].x()))
            self.tableWidget.setItem(i,1,itemE)
            itemN = QTableWidgetItem(str(self.points[i].y()))            
            self.tableWidget.setItem(i,2,itemN)

            if (i == len(distancesAndAzimuths) - 1) and isClosed:
                itemSide = QTableWidgetItem("Pt"+str(i)+"-Pt0")
                self.tableWidget.setItem(i,3,itemSide)
            else:
                itemSide = QTableWidgetItem("Pt"+str(i)+"-Pt"+str(i+1))
                self.tableWidget.setItem(i,3,itemSide)

            itemAz = QTableWidgetItem(azimuth)
            self.tableWidget.setItem(i,4,itemAz)
            itemRealAz = QTableWidgetItem(realAzimuth)
            self.tableWidget.setItem(i,5,itemRealAz)
            dist = "%0.2f"%(distancesAndAzimuths[i][0])            
            itemDistance = QTableWidgetItem(dist)
            self.tableWidget.setItem(i,6,itemDistance)
            itemConfronting = QTableWidgetItem("")
            self.tableWidget.setItem(i,7,itemConfronting)
        
    def clearTextEdit(self):
        self.textEdit.clear()
        
    def dd2dms(self, dd):
        d = int(dd)
        m = abs(int(60*(dd-int(dd))))
        s = abs((dd-d-m/60)*60)
        dms = str(d) + u"\u00b0" + str(m).zfill(2) + "'" + "%0.2f"%(s) + "''"
        return dms
        
