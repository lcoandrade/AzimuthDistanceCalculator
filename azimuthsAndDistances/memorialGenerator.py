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
import shutil
import os
import time
import sys

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_memorialGenerator.ui'))

reload(sys)  
sys.setdefaultencoding('utf-8')

class MemorialGenerator(QDialog, FORM_CLASS):
    
    def __init__(self, crsDescription, centralMeridian, convergence, tableWidget, geomArea, geomPerimeter):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        # Connecting SIGNAL/SLOTS for the Output button
        self.folderButton.clicked.connect(self.setDirectory)

        # Connecting SIGNAL/SLOTS for the Output button
        self.createButton.clicked.connect(self.createFiles)

        self.convergenciaEdit.setText(convergence)
        
        self.tableWidget = tableWidget
        self.geomArea = geomArea
        self.geomPerimeter = geomPerimeter

        self.meridianoEdit.setText(str(centralMeridian))
        self.projectionEdit.setText(crsDescription.split('/')[-1])
        self.datumEdit.setText(crsDescription.split('/')[0])
        
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

        QMessageBox.information(self, self.tr('Information!'), self.tr('Files created successfully!'))
        
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
        
        element = tempDoc.documentElement()
         
        nodes = element.elementsByTagName("table")
         
        table = nodes.item(0).toElement()

        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, u"MEMORIAL DESCRITIVO SINTÉTICO", 7, 0))
        table.appendChild(tr)
        
        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, u"VÉRTICE", 0, 2))
        tr.appendChild(self.createCellElement(tempDoc, "COORDENADAS", 2, 0))
        tr.appendChild(self.createCellElement(tempDoc, "LADO", 0, 2))
        tr.appendChild(self.createCellElement(tempDoc, "AZIMUTES", 2, 0))
        tr.appendChild(self.createCellElement(tempDoc, u"DISTÂNCIA", 0, 0))
        table.appendChild(tr)
        
        tr = tempDoc.createElement("tr")
        tr.appendChild(self.createCellElement(tempDoc, "E", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "N", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "PLANO", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "REAL", 0, 0))
        tr.appendChild(self.createCellElement(tempDoc, "(m)", 0, 0))
        table.appendChild(tr)
         
        convergence = float(self.convergenciaEdit.text())
             
        rowCount = self.tableWidget.rowCount()
        
        for i in xrange(0,rowCount):
            lineElement = tempDoc.createElement("tr")
             
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,0).text(), 0, 0))
             
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,1).text(), 0, 0))
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,2).text(), 0, 0))
 
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,3).text(), 0, 0))
 
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,4).text(), 0, 0))
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,5).text(), 0, 0))
            lineElement.appendChild(self.createCellElement(tempDoc, self.tableWidget.item(i,6).text(), 0, 0))
            
            table.appendChild(lineElement)
            
        simple = open(self.simpleMemorial, "w")
        simple.write(tempDoc.toString())
        simple.close()
        
    def createArea(self):
        area = open(self.area, "r")
        fileData = area.read()
        area.close()

        kappa = float(self.kappaEdit.text())
        
        newData = fileData.replace("[IMOVEL]", self.imovelEdit.text())
        newData = newData.replace("[PROPRIETARIO]", self.proprietarioEdit.text())
        newData = newData.replace("[MUNICIPIO]", self.municipioEdit.text())
        newData = newData.replace("[COMARCA]", self.comarcaEdit.text())
        newData = newData.replace("[DATUM]", self.datumEdit.text())
        newData = newData.replace("[MERIDIANO]", self.meridianoEdit.text())
        newData = newData.replace("[KAPPA]", self.kappaEdit.text())
        geomPerimeter = self.geomPerimeter/kappa
        newData = newData.replace("[PERIMETRO]", "%0.2f"%(geomPerimeter))
        geomArea = self.geomArea/(kappa*kappa)
        newData = newData.replace("[AREA]", "%0.2f"%(geomArea))
        
        newData += "\n"
        newData += "\n"
        newData += "\n"
        
        newData += "Estação    Vante    Coordenada E    Coordenada N    Az Plano    Az Real    Distância\n"
        
        rowCount = self.tableWidget.rowCount()
        
        for i in xrange(0,rowCount):            
            line  = str()
            side = self.tableWidget.item(i,3).text()
            sideSplit = side.split("-")
            line += sideSplit[0]+"    "+sideSplit[1]+"    "
            line += self.tableWidget.item(i,1).text()+"    "
            line += self.tableWidget.item(i,2).text()+"    "
            line += self.tableWidget.item(i,4).text()+"    "
            line += self.tableWidget.item(i,5).text()+"    "
            line += self.tableWidget.item(i,6).text()+"\n"
            
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

        kappa = float(self.kappaEdit.text())
        
        newData = fileData.replace("[IMOVEL]", self.imovelEdit.text())
        newData = newData.replace("[PROPRIETARIO]", self.proprietarioEdit.text())
        newData = newData.replace("[UF]", self.ufEdit.text())
        newData = newData.replace("[COD_INCRA]", self.codIncraEdit.text())
        geomPerimeter = self.geomPerimeter/kappa
        newData = newData.replace("[PERIMETRO]", "%0.2f"%(geomPerimeter))
        geomArea = self.geomArea/(kappa*kappa)
        newData = newData.replace("[AREA]", "%0.2f"%(geomArea))
        newData = newData.replace("[COMARCA]", self.comarcaEdit.text())
        newData = newData.replace("[MUNICIPIO]", self.municipioEdit.text())
        newData = newData.replace("[MATRICULA]", self.matriculaEdit.text())
        newData = newData.replace("[DESCRIPTION]", self.getDescription())
        newData = newData.replace("[DATA]", time.strftime("%d/%m/%Y"))
        newData = newData.replace("[AUTOR]", self.autorEdit.text())
        newData = newData.replace("[CREA]", self.creaEdit.text())
        newData = newData.replace("[CREDENCIAMENTO]", self.credenciamentoEdit.text())
        newData = newData.replace("[ART]", self.artEdit.text())
        
        memorial = open(self.fullMemorial, "w")
        memorial.write(newData)
        memorial.close()
        
    def getDescription(self):
        description = str()
        description += "Inicia-se a descrição deste perímetro no vértice "+self.tableWidget.item(0,0).text()+", de coordenadas "
        description += "N "+self.tableWidget.item(0,2).text()+" m e "
        description += "E "+self.tableWidget.item(0,1).text()+" m, "
        description += "Datum " +self.datumEdit.text()+ " com Meridiano Central " +self.meridianoEdit.text()+ ", localizado a "+self.enderecoEdit.text()+", Código INCRA " +self.codIncraEdit.text()+ "; "

        rowCount = self.tableWidget.rowCount()            
        for i in xrange(0,rowCount):
            side = self.tableWidget.item(i,3).text()
            sideSplit = side.split("-")

            description += " deste, segue confrontando com "+self.tableWidget.item(i,7).text()+", "
            description += "com os seguintes azimute plano e distância:"
            description += self.tableWidget.item(i,4).text()+" e "
            description += self.tableWidget.item(i,6).text()+"; até o vértice "
            if (i == rowCount - 1):
                description += sideSplit[1]+", de coordenadas "
                description += "N "+self.tableWidget.item(0,2).text()+" m e "
                description += "E "+self.tableWidget.item(0,1).text()+" m, encerrando esta descrição."
                description += " Todas as coordenadas aqui descritas estão georrefereciadas ao Sistema Geodésico Brasileiro, "
                description += "a partir da estação RBMC de "+self.rbmcOrigemEdit.text()+" de coordenadas "
                description += "E "+self.rbmcEsteEdit.text()+" m e N "+self.rbmcNorteEdit.text()+" m, "
                description += "localizada em "+self.localRbmcEdit.text()+", "
                description += "e encontram-se representadas no sistema UTM, referenciadas ao Meridiano Central "+self.meridianoEdit.text()
                description += ", tendo como DATUM "+self.datumEdit.text()+"."
                description += "Todos os azimutes e distâncias, área e perímetro foram calculados no plano de projeção UTM."
            else:
                description += sideSplit[1]+", de coordenadas "
                description += "N "+self.tableWidget.item(i+1,2).text()+" m e "
                description += "E "+self.tableWidget.item(i+1,1).text()+" m;"
                
        return description
