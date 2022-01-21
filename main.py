#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import os
from run_greedy import run_greedy
from generateGraph import graphGenerator
from algorithms import run_linear_determinist

from PyQt5.QtGui import QIcon, QCursor, QIntValidator
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel,
        QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout,
        QProgressBar, QPushButton, QRadioButton, QLineEdit,
        QStyleFactory, QTextEdit, QFileDialog)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        screenSize = app.primaryScreen().size()
        # print('Size: %d x %d' % (screenSize.width(), screenSize.height()))
        self.setFixedWidth(screenSize.width()*0.4)
        self.setFixedHeight(screenSize.height()*0.7)

        self.setWindowTitle("FraudAdvisor")
        self.setWindowIcon(QIcon('logo_fraudadvisor.png'))
        self.changeStyle('Fusion')

        outputLabel = QLabel("<h2>Output</h2>")

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Le résultat des opérations s'afficheront ici.\n")
        self.textEdit.setReadOnly(True)

        btnClear = QPushButton("Effacer\nla sortie", cursor=QCursor(Qt.PointingHandCursor))
        btnClear.setIcon(QApplication.style().standardIcon(QApplication.style().SP_DialogResetButton))

        self.createLeftGroupBox()
        self.createRightGroupBox()
        self.createBottomGroupBox()
        self.createProgressBar()

        btnClear.clicked.connect(self.textEdit.clear)


        outputLayout = QVBoxLayout()
        outputLayout.addWidget(outputLabel)
        outputLayout.addWidget(self.textEdit)
        topLayout = QHBoxLayout()
        topLayout.addLayout(outputLayout)
        topLayout.addWidget(btnClear)


        # rbDataset = QRadioButton("Dataset", cursor=QCursor(Qt.PointingHandCursor))
        # rbGraph = QRadioButton("Graphe aléatoire", cursor=QCursor(Qt.PointingHandCursor))
        # rbDataset.toggled.connect(self.leftGroupBox.setDisabled)
        # rbGraph.toggled.connect(self.bottomLeftGroupBox.setDisabled)

        # inputModeLayout = QHBoxLayout()
        # inputModeLayout.addWidget(rbDataset)
        # inputModeLayout.addWidget(rbGraph)
        
        # outputLayout.addLayout(inputModeLayout)


        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.rightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomGroupBox, 2, 0, 1, 2)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)
        self.setStyleSheet('QGroupBox { font-weight: bold; }')
        self.selectedDataset = ''

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        QApplication.setPalette(QApplication.style().standardPalette())

    def selectFile(self):
        file_filter = 'Text files (*.txt)' # 'Text files (*.txt);;Data File (*.xlsx *.csv *.dat)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Selectionnez un dataset',
            directory=os.getcwd(),
            filter=file_filter
        )
        print(response)

        if response[0] != '':
            self.selectedDataset = response[0]
            self.textEdit.append("----------------------------------------------")
            self.textEdit.append("Vous avez sélectionné le dataset : " + self.selectedDataset + "\n")
        return response[0]

    def runGraphGenerator(self, nbNode, nbEdge):
        if nbNode != '' and nbEdge != '':
            nbNode = int(nbNode)
            nbEdge = int(nbEdge)
            print(nbNode, nbEdge, nbNode+nbEdge)
            self.selectedDataset = graphGenerator(nbNode, nbEdge)
            self.textEdit.append("----------------------------------------------")
            self.textEdit.append("Vous avez généré le dataset : " + self.selectedDataset + "\n")
            self.textEdit.append("Ce dataset est désormais sélectionné.\n")

    def updateAlgo(self, algo):
        self.algo = algo

    def runAlgo(self):
        """TODO: understand why computing wipes out previous UI instructions.."""
        self.toggleGroupBoxesAvailability()

        if self.selectedDataset == '':
            self.textEdit.append("Impossible de lancer l'algo, aucun dataset n'est sélectionné.\n")
            self.toggleGroupBoxesAvailability()
            return

        self.textEdit.append("==============================================\n")
        self.textEdit.append("Lancement de l'algorithme " + self.algo + "...\n")

        if self.algo == "fraudar":
            score = run_greedy(self.selectedDataset, "out/out")
            self.textEdit.append("Le score obtenu est " + str(score) + ".\n")
        elif self.algo == "linear":
            res = run_linear_determinist(self.selectedDataset)
            self.textEdit.append("Le résultat obtenu est " + str(res) + ".\n")
        elif self.algo == "stocha":
            # res = run_stocha(self.selectedDataset)
            self.textEdit.append("TODO : bind l'algo stochastique.\n")
            # self.textEdit.append("Le résultat obtenu est " + str(res) + ".\n")
        else:
            pass
        
        self.textEdit.append("Les résultats sont dans le dossier out.\n")

        self.toggleGroupBoxesAvailability()

    def toggleGroupBoxesAvailability(self):
        oldleft = self.leftGroupBox.isEnabled()
        oldright = self.rightGroupBox.isEnabled()

        self.leftGroupBox.setDisabled(oldleft)
        self.rightGroupBox.setDisabled(oldright)

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox("Dataset")

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        dataLabel = QLabel("Sélectionnez le dataset à utiliser :")

        loadDataBtn = QPushButton("Charger le dataset ⬇", cursor=QCursor(Qt.PointingHandCursor))
        # loadDataBtn.setFlat(True)
        loadDataBtn.setIcon(QApplication.style().standardIcon(QApplication.style().SP_DirLinkIcon))
        loadDataBtn.setIconSize(QSize(50,50))
        loadDataBtn.clicked.connect(self.selectFile)

        layout.addWidget(dataLabel)
        layout.addStretch(1)
        layout.addWidget(loadDataBtn)
        layout.addStretch(1)

        self.leftGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox("Générer un graphe aléatoire")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        layoutNode = QHBoxLayout()
        rangeLabel = QLabel("Nombre de noeuds à générer :")
        rangeNode = QLineEdit()
        rangeNode.setValidator(QIntValidator())
        rangeNode.setMaxLength(3)

        layoutEdge = QHBoxLayout()
        rangeEdgeLabel = QLabel("Nombre d'arêtes à générer :")
        rangeEdge = QLineEdit()
        rangeEdge.setValidator(QIntValidator())
        rangeEdge.setMaxLength(3)
        
        runGraphGen = QPushButton("Générer ⚙", cursor=QCursor(Qt.PointingHandCursor))
        runGraphGen.clicked.connect(lambda: self.runGraphGenerator(rangeNode.text(), rangeEdge.text()))

        layoutNode.addWidget(rangeLabel)
        layoutNode.addWidget(rangeNode)
        layoutEdge.addWidget(rangeEdgeLabel)
        layoutEdge.addWidget(rangeEdge)

        layout.addLayout(layoutNode)
        layout.addLayout(layoutEdge)
        layout.addWidget(runGraphGen)


        self.rightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Execution")

        runLabel = QLabel("Algorithme de détection de fraude :")

        radioBtn1 = QRadioButton("fBOX", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn1.setDisabled(True)
        radioBtn2 = QRadioButton("FRAUDAR", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn2.setChecked(True)
        self.algo = "fraudar"
        radioBtn3 = QRadioButton("Le nôtre (linéaire)", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn4 = QRadioButton("Le nôtre (stochastique)", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn2.toggled.connect(lambda: self.updateAlgo("fraudar"))
        radioBtn3.toggled.connect(lambda: self.updateAlgo("linear"))
        radioBtn4.toggled.connect(lambda: self.updateAlgo("stocha"))

        runAlgoBtn = QPushButton("Lancer ⚙", cursor=QCursor(Qt.PointingHandCursor))
        runAlgoBtn.setDefault(True)
        runAlgoBtn.clicked.connect(self.runAlgo)

        layout = QVBoxLayout()

        rbLayout = QGridLayout()
        rbLayout.addWidget(radioBtn1, 1, 1)
        rbLayout.addWidget(radioBtn2, 2, 1)
        rbLayout.addWidget(radioBtn3, 1, 2)
        rbLayout.addWidget(radioBtn4, 2, 2)

        rbLayout.setColumnStretch(0, 10)
        rbLayout.setColumnStretch(1, 10)
        rbLayout.setColumnStretch(2, 10)
        rbLayout.setColumnStretch(3, 10)

        layout.addWidget(runLabel)
        layout.addLayout(rbLayout)
        layout.addWidget(runAlgoBtn)
        layout.addStretch(1)
        self.bottomGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)


if __name__ == '__main__':

    import sys

    # Tells explicitly to OS what the correct process ID is (for displaying app logo in taskbar too)
    import ctypes
    myappid = 'fr.polytech.fraudadvisor.0.0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()

    sys.exit(app.exec_()) 
