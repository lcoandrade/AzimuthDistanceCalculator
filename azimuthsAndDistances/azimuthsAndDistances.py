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
from PyQt4.QtGui import QDialog, QTableWidgetItem, QMessageBox
from qgis.core import QGis

import math

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_azimuthsAndDistances.ui'))

from AzimuthDistanceCalculator.azimuthsAndDistances.memorialGenerator import MemorialGenerator
from AzimuthDistanceCalculator.kappaAndConvergence.calculateKappaAndConvergence import CalculateKappaAndConvergenceDialog

class AzimuthsAndDistancesDialog(QDialog, FORM_CLASS):
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
        self.calculateButton.clicked.connect(self.fillTable)
        self.clearButton.clicked.connect(self.clearTable)
        self.saveFilesButton.clicked.connect(self.saveFiles)
        self.convergenceButton.clicked.connect(self.calculateConvergence)

        self.lineEdit.setInputMask("#00.00000")

    def calculateConvergence(self):
        convergenceCalculator = CalculateKappaAndConvergenceDialog(self.iface)
        (a, b) = convergenceCalculator.getSemiMajorAndSemiMinorAxis()

        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            selectedFeatures = len(currentLayer.selectedFeatures())
            if selectedFeatures == 1:
                selectedFeature = currentLayer.selectedFeatures()[0]

                centroid = selectedFeature.geometry().centroid()
                geoPoint = convergenceCalculator.getGeographicCoordinates(centroid.asPoint().x(), centroid.asPoint().y())
                self.centralMeridian = convergenceCalculator.getCentralMeridian(geoPoint.x())

                convergence = convergenceCalculator.calculateConvergence2(geoPoint.x(), geoPoint.y(), a, b)

                self.lineEdit.setText(str(convergence))

    def setClockWiseRotation(self, points):
        sum = 0
        for i in xrange(len(points) - 1):
            sum += (points[i+1].x() - points[i].x())*(points[i+1].y() - points[i].y())

        if sum > 0:
            return points
        else:
            return points[::-1]

    def setFirstPointToNorth(self, coords, yMax):
        if coords[0].y() == yMax:
            return coords

        coords.pop()
        firstPart = []
        for i in range(len(coords)):
            firstPart.append(coords[i])
            if coords[i].y() == yMax:
                break

        return coords[i:] + firstPart

    def saveFiles(self):
        if (not self.distancesAndAzimuths) or (not self.points):
            QMessageBox.information(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Click on calculate button first to generate the needed data."))
        else:
            confrontingList = list()
            for i in xrange(self.tableWidget.rowCount()):
                item = self.tableWidget.item(i, 7)
                confrontingList.append(item.text())

            d = MemorialGenerator(self.iface.mapCanvas().currentLayer().crs().description(), self.centralMeridian, self.lineEdit.text(), self.tableWidget, self.area, self.perimeter)
            d.exec_()

    def isValidType(self):
        """Verifies the geometry type.
        """
        if self.geom.isMultipart():
            QMessageBox.information(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The limit of a patrimonial area must be a single part geometry."))
            return False

        if self.geom.type() == QGis.Line:
            self.points = self.geom.asPolyline()
            if self.points[0].y() < self.points[-1].y():
                self.points = self.points[::-1]
            return True
        elif self.geom.type() == QGis.Polygon:
            points = self.setClockWiseRotation(self.geom.asPolygon()[0])
            yMax = self.geom.boundingBox().yMaximum()
            self.points = self.setFirstPointToNorth(points, yMax)
            return True
        else:
            QMessageBox.information(self.iface.mainWindow(), self.tr("Warning!"), self.tr("The selected geometry should be a Line or a Polygon."))
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
            if azimuth < 0:
                azimuth += 360
            self.distancesAndAzimuths.append((distance, azimuth))
            self.perimeter += distance

        return self.distancesAndAzimuths

    def fillTable(self):
        """Makes the CSV.
        """
        distancesAndAzimuths = list()
        isValid = self.isValidType()
        if isValid:
            distancesAndAzimuths = self.calculate()
        try:
            convergence = float(self.lineEdit.text())
        except ValueError:
            QMessageBox.information(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please, insert the meridian convergence."))
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

    def clearTable(self):
        self.tableWidget.setRowCount(0)

    def dd2dms(self, dd):
        is_positive = dd >= 0
        dd = abs(dd)
        minutes,seconds = divmod(dd*3600,60)
        degrees,minutes = divmod(minutes,60)

        degrees = str(int(degrees)) if is_positive else '-' + str(int(degrees))
        minutes = int(minutes)

        return degrees + u"\u00b0" + str(minutes).zfill(2) + "'" + "%0.2f"%(seconds) + "''"        