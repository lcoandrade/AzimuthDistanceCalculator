# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Memorial Generator
# Purpose:
#
# Author:      Luiz Andrade - luiz.claudio@dsg.eb.mil.br
#
# Created:     30/09/2014
# Copyright:   (c) luiz 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtXml import *

import math
import shutil
import os

from ui_memorialGenerator import Ui_Dialog

# encoding=latin-1  
import sys  

reload(sys)  
sys.setdefaultencoding('utf-8')

import time

class MemorialGenerator( QDialog, Ui_Dialog ):
    
    def __init__(self, convergence, distancesAndAzimuths, points, confrontingList, geomArea, geomPerimeter):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.folderButton, SIGNAL("clicked()"), self.setDirectory)        

        # Connecting SIGNAL/SLOTS for the Output button
        QObject.connect(self.createButton, SIGNAL("clicked()"), self.createFiles)        
        
        self.convergenciaEdit.setText(convergence)
        
        self.distancesAndAzimuths = distancesAndAzimuths
        self.points = points
        self.confrontingList = confrontingList
        self.geomArea = geomArea
        self.geomPerimeter = geomPerimeter
        
    def setDirectory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.folderEdit.setText(folder)
        
    def copyAndRenameFiles(self):
        currentPath = os.path.dirname(__file__)
        templatePath = os.path.join(currentPath, "templates")
        simpleMemorialTemplate = os.path.join(templatePath, "template_sintetico.html")
        fullMemorialTemplate = os.path.join(templatePath, "template_memorial.txt")
        seloTemplate = os.path.join(templatePath, "template_selo.txt")
        areaTemplate = os.path.join(templatePath, "template_area.txt")
        
        folder = self.folderEdit.text()
        self.simpleMemorial = os.path.join(folder, "sintetico.html")
        self.fullMemorial = os.path.join(folder, "analitico.txt")
        self.selo = os.path.join(folder, "selo.txt")
        self.area = os.path.join(folder, "area.txt")
        
        shutil.copy2(simpleMemorialTemplate, self.simpleMemorial)
        shutil.copy2(fullMemorialTemplate, self.fullMemorial)
        shutil.copy2(seloTemplate, self.selo)
        shutil.copy2(areaTemplate, self.area)
        
    def createFiles(self):
        self.copyAndRenameFiles()
        
        self.createSelo()
        
        self.createFullMemorial()
        
        self.createArea()
        
        self.createSimpleMemorial()
        
    def createCellElement(self, tempDoc, text, colspan, rowspan):
        td = tempDoc.createElement("td")
        p = tempDoc.createElement("p")
        span = tempDoc.createElement("span")

        if colspan > 0:
            td.setAttribute("colspan", colspan)
        if rowspan > 0:
            td.setAttribute("rowspan", rowspan)
        td.setAttribute("style", "border-color : #000000 #000000 #000000 #000000; border-style: solid;")
        p.setAttribute("style", " text-align: center; text-indent: 0px; padding: 0px 0px 0px 0px; margin: 0px 0px 0px 0px;")
        span.setAttribute("style", " font-size: 10pt; font-family: 'Arial', 'Helvetica', sans-serif; font-style: normal; font-weight: normal; color: #000000; background-color: transparent; text-decoration: none;")
        
        textElement = tempDoc.createTextNode(text)
        
        span.appendChild(textElement)
        p.appendChild(span)
        td.appendChild(p)
        
        return td
        
    def createSimpleMemorial(self):
        tempDoc = QDomDocument()
        simple = QFile(self.simpleMemorial)
        simple.open(QIODevice.ReadOnly)
        loaded = tempDoc.setContent(simple)
        simple.close()
        
        print loaded
        
        element = tempDoc.documentElement()
         
        nodes = element.elementsByTagName("table")
         
        table = nodes.item(0).toElement()

        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, "MEMORIAL DESCRITIVO SINTETICO", 7, 0))
        table.appendChild(tr)
        
        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, "VERTICE", 0, 2))
        tr.appendChild(self.createCellElement(tempDoc, "COORDENADAS", 2, 0))
        tr.appendChild(self.createCellElement(tempDoc, "LADO", 0, 2))
        tr.appendChild(self.createCellElement(tempDoc, "AZIMUTES", 2, 0))
        tr.appendChild(self.createCellElement(tempDoc, "DISTANCIA", 0, 0))
        table.appendChild(tr)
        
        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, "E", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "N", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "PLANO", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "REAL", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "(m)", 0, 0))
        table.appendChild(tr)
         
        convergence = float(self.convergenciaEdit.text())
             
        isClosed = False
        if self.points[0] == self.points[len(self.points) - 1]:
            isClosed = True
 
        for i in xrange(0,len(self.distancesAndAzimuths)):
            lineElement = tempDoc.createElement("tr")
             
            azimuth = self.dd2dms(self.distancesAndAzimuths[i][1])
            realAzimuth = self.dd2dms(self.distancesAndAzimuths[i][1] + convergence)
             
            lineElement.appendChild(self.createCellElement(tempDoc, "Pt"+str(i), 0, 0))
             
            lineElement.appendChild(self.createCellElement(tempDoc, str(self.points[i].x()), 0, 0))
            lineElement.appendChild(self.createCellElement(tempDoc, str(self.points[i].y()), 0, 0))
 
            if (i == len(self.distancesAndAzimuths) - 1) and isClosed:
                lineElement.appendChild(self.createCellElement(tempDoc, "Pt"+str(i)+"-Pt0", 0, 0))
            else:
                lineElement.appendChild(self.createCellElement(tempDoc, "Pt"+str(i)+"-Pt"+str(i+1), 0, 0))
 
            lineElement.appendChild(self.createCellElement(tempDoc, azimuth, 0, 0))
            lineElement.appendChild(self.createCellElement(tempDoc, realAzimuth, 0, 0))
            dist = "%0.2f"%(self.distancesAndAzimuths[i][0])            
            lineElement.appendChild(self.createCellElement(tempDoc, dist, 0, 0))
            
            table.appendChild(lineElement)
            
        simple = open(self.simpleMemorial, "w")
        simple.write(tempDoc.toString())
        simple.close()
        
    def createArea(self):
        isClosed = False
        if self.points[0] == self.points[len(self.points) - 1]:
            isClosed = True
        
        area = open(self.area, "r")
        fileData = area.read()
        area.close()
        
        newData = fileData.replace("[IMOVEL]", self.imovelEdit.text())
        newData = newData.replace("[PROPRIETARIO]", self.proprietarioEdit.text())
        newData = newData.replace("[MUNICIPIO]", self.municipioEdit.text())
        newData = newData.replace("[COMARCA]", self.comarcaEdit.text())
        newData = newData.replace("[DATUM]", self.datumEdit.text())
        newData = newData.replace("[MERIDIANO]", self.meridianoEdit.text())
        newData = newData.replace("[KAPPA]", self.kappaEdit.text())
        geomPerimeter = self.geomPerimeter*(float(self.kappaEdit.text()))
        newData = newData.replace("[PERIMETRO]", "%0.2f"%(geomPerimeter))
        geomArea = self.geomArea*(float(self.kappaEdit.text()))*(float(self.kappaEdit.text()))
        newData = newData.replace("[AREA]", "%0.2f"%(geomArea))
        
        newData += "\n"
        newData += "\n"
        newData += "\n"
        
        newData += "Estação    Vante    Coordenada E    Coordenada N    Az Plano    Az Real    Distância\n"
        
        for i in xrange(0,len(self.distancesAndAzimuths) - 1):            
            azimuth = self.dd2dms(self.distancesAndAzimuths[i][1])
            realAzimuth = self.dd2dms(self.distancesAndAzimuths[i][1] + float(self.convergenciaEdit.text()))

            line  = str()
            line += "Pt"+str(i)+"    "
            if (i == len(self.distancesAndAzimuths) - 2) and isClosed:
                line += "Pt0    "
            else:
                line += "Pt"+str(i+1)+"    "                
            line += str(self.points[i].x())+"    "
            line += str(self.points[i].y())+"    "
            line += azimuth+"    "
            line += realAzimuth+"    "
            dist = "%0.2f"%(self.distancesAndAzimuths[i][0])
            line += str(dist)+"\n"
            
            newData += line

        area = open(self.area, "w")
        area.write(newData)
        area.close()
        
    def createSelo(self):
        memorial = open(self.selo, "r")
        fileData = memorial.read()
        memorial.close()
        
        newData = fileData.replace("[IMOVEL]", self.imovelEdit.text())
        newData = newData.replace("[CADASTRO]", self.cadastroEdit.text())
        newData = newData.replace("[PROPRIETARIO]", self.proprietarioEdit.text())
        newData = newData.replace("[UF]", self.ufEdit.text())
        newData = newData.replace("[MATRICULA]", self.matriculaEdit.text())
        newData = newData.replace("[PROJECAO]", self.projectionEdit.text())
        newData = newData.replace("[KAPPA]", self.kappaEdit.text())
        newData = newData.replace("[DATUM]", self.datumEdit.text())
        
        memorial = open(self.selo, "w")
        memorial.write(newData)
        memorial.close()

    def createFullMemorial(self):
        memorial = open(self.fullMemorial, "r")
        fileData = memorial.read()
        memorial.close()
        
        newData = fileData.replace("[IMOVEL]", self.imovelEdit.text())
        newData = newData.replace("[PROPRIETARIO]", self.proprietarioEdit.text())
        newData = newData.replace("[UF]", self.ufEdit.text())
        newData = newData.replace("[COD_INCRA]", self.codIncraEdit.text())
        geomPerimeter = self.geomPerimeter*(float(self.kappaEdit.text()))
        newData = newData.replace("[PERIMETRO]", "%0.2f"%(geomPerimeter))
        geomArea = self.geomArea*(float(self.kappaEdit.text()))*(float(self.kappaEdit.text()))
        newData = newData.replace("[AREA]", "%0.2f"%(geomArea))
        newData = newData.replace("[COMARCA]", self.comarcaEdit.text())
        newData = newData.replace("[MUNICIPIO]", self.municipioEdit.text())
        newData = newData.replace("[MATRICULA]", self.matriculaEdit.text())
        newData = newData.replace("[DESCRIPTION]", self.getDescription())
        newData = newData.replace("[DATA]", time.strftime("%d/%m/%Y"))
        newData = newData.replace("[AUTOR]", self.autorEdit.text())
        newData = newData.replace("[CREA]", self.creaEdit.text())
        
        memorial = open(self.fullMemorial, "w")
        memorial.write(newData)
        memorial.close()
        
    def getDescription(self):
        isClosed = False
        if self.points[0] == self.points[len(self.points) - 1]:
            isClosed = True
        
        description = str()
        description += "Inicia-se a descrição deste perímetro no vértice Pt0, de coordenadas "
        description += "N "+str(self.points[0].y())+" m e "
        description += "E "+str(self.points[0].x())+" m, "
        description += "Datum " +self.datumEdit.text()+ " com Meridiano Central " +self.meridianoEdit.text()+ ", localizado a "+self.enderecoEdit.text()+", Código INCRA " +self.codIncraEdit.text()+ "; "
            
        for i in xrange(0,len(self.distancesAndAzimuths)):
            azimuth = self.dd2dms(self.distancesAndAzimuths[i][1])

            description += " deste, segue confrontando com "+self.confrontingList[i]+", "
            description += "com os seguintes azimute plano e distância:"
            description += azimuth+" e "
            dist = "%0.2f"%(self.distancesAndAzimuths[i][0])
            description += str(dist)+"; até o vértice "
            if (i == len(self.distancesAndAzimuths) - 1) and isClosed:
                description += "Pt0, de coordenadas "
                description += "N "+str(self.points[0].y())+" m e "
                description += "E "+str(self.points[0].x())+" m, encerrando esta descrição."
            elif (i == len(self.distancesAndAzimuths) - 1) and isClosed == False:
                description += "Pt"+str(i+1)+", de coordenadas "
                description += "N "+str(self.points[i+1].y())+" m e "
                description += "E "+str(self.points[i+1].x())+" m, encerrando esta descrição."
            else:
                description += "Pt"+str(i+1)+", de coordenadas "
                description += "N "+str(self.points[i+1].y())+" m e "
                description += "E "+str(self.points[i+1].x())+" m;"
                
        return description
                    
    def dd2dms(self, dd):
        dd = float(dd)
        d = int(dd)
        m = abs(int(60*(dd-d)))
        s = abs((dd-d-m/60)*60)
        dms = str(d) + u"\u00b0" + str(m).zfill(2) + "'" + "%0.2f"%(s) + "''"
        return dms
        
