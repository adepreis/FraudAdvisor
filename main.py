#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is INSPIRED BY examples of PyQt (from https://github.com/pyqt/examples).
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
from algorithms import run_linear
from graph_generation import graphGenerator

from PyQt5.QtGui import QIcon, QCursor, QIntValidator
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel,
        QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton,
        QRadioButton, QLineEdit, QStyleFactory, QTextEdit, QFileDialog)

class FraudAdvisorUI(QMainWindow):
    def __init__(self, parent=None):
        super(FraudAdvisorUI, self).__init__(parent)

        screenSize = app.primaryScreen().size()
        # print('Size: %d x %d' % (screenSize.width(), screenSize.height()))
        self.setFixedWidth(screenSize.width()*0.4)
        self.setFixedHeight(screenSize.height()*0.7)

        self.setWindowTitle("FraudAdvisor")
        self.setWindowIcon(QIcon('logo_fraudadvisor.png'))
        self.changeStyle('Fusion')

        outputLabel = QLabel("<h2>Output</h2>")

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Le r??sultat des op??rations s'afficheront ici.\n")
        self.textEdit.setReadOnly(True)

        btnClear = QPushButton("Effacer\nla sortie", cursor=QCursor(Qt.PointingHandCursor))
        btnClear.setIcon(QApplication.style().standardIcon(QApplication.style().SP_DialogResetButton))

        self.createLeftGroupBox()
        self.createRightGroupBox()
        self.createBottomGroupBox()

        btnClear.clicked.connect(self.textEdit.clear)


        outputLayout = QVBoxLayout()
        outputLayout.addWidget(outputLabel)
        outputLayout.addWidget(self.textEdit)
        topLayout = QHBoxLayout()
        topLayout.addLayout(outputLayout)
        topLayout.addWidget(btnClear)


        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.rightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomGroupBox, 2, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        window = QWidget()
        window.setLayout(mainLayout)
        # QMainWindow needs a central widget as it already has predefined layout:
        self.setCentralWidget(window)
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
            self.textEdit.append("Vous avez s??lectionn?? le dataset : " + self.selectedDataset + "\n")
        return response[0]

    def runGraphGenerator(self, nbNode, nbEdge):
        if nbNode != '' and nbEdge != '':
            self.selectedDataset = graphGenerator(int(nbNode), int(nbEdge))
            self.textEdit.append("----------------------------------------------")
            self.textEdit.append("Vous avez g??n??r?? le graphe : " + self.selectedDataset + \
                                " (" + nbNode + " noeuds, " + nbEdge + " ar??tes)\n")
            self.textEdit.append("Ce graphe est d??sormais s??lectionn?? en tant que dataset.\n")

    def updateAlgo(self, algo):
        self.algo = algo

    def runAlgo(self):
        """TODO: understand why computing wipes out previous UI instructions.."""
        self.toggleGroupBoxesAvailability()

        if self.selectedDataset == '':
            self.textEdit.append("Impossible de lancer l'algo, aucun dataset n'est s??lectionn??.\n")
            self.toggleGroupBoxesAvailability()
            return

        self.textEdit.append("==============================================\n")
        self.textEdit.append("Lancement de l'algorithme " + self.algo + "...\n")

        succeeded, res = False, "Une erreur a mis fin ?? l'execution de l'algorithme.\n"

        if self.algo == "fraudar":
            succeeded, res = run_greedy(self.selectedDataset, "out/out")
        elif self.algo == "deterministic":
            succeeded, res = run_linear(self.selectedDataset, stochastic=False)
        elif self.algo == "stochastic":
            succeeded, res = run_linear(self.selectedDataset, stochastic=True) # different parameter but same constraints
        else:
            pass
        
        
        # Guide user to algo output if there is a score
        if succeeded:
            self.textEdit.append("Le r??sultat obtenu est " + str(res) + ".\n")
            self.textEdit.append("Les r??sultats sont dans le dossier out.\n")
        else:
            self.textEdit.append("Erreur : " + str(res) + ".\n")

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

        dataLabel = QLabel("S??lectionnez le dataset ?? utiliser :")

        loadDataBtn = QPushButton("Charger le dataset ???", cursor=QCursor(Qt.PointingHandCursor))
        loadDataBtn.setIcon(QApplication.style().standardIcon(QApplication.style().SP_DirLinkIcon))
        loadDataBtn.setIconSize(QSize(50,50))
        loadDataBtn.clicked.connect(self.selectFile)

        layout.addWidget(dataLabel)
        layout.addStretch(1)
        layout.addWidget(loadDataBtn)
        layout.addStretch(1)

        self.leftGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox("G??n??rer un graphe al??atoire")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        rangeLabel = QLabel("Nombre de noeuds ?? g??n??rer :")
        rangeNode = QLineEdit()
        rangeNode.setValidator(QIntValidator())
        rangeNode.setMaxLength(3)

        rangeEdgeLabel = QLabel("Nombre d'ar??tes ?? g??n??rer :")
        rangeEdge = QLineEdit()
        rangeEdge.setValidator(QIntValidator())
        rangeEdge.setMaxLength(3)
        
        runGraphGen = QPushButton("G??n??rer ???", cursor=QCursor(Qt.PointingHandCursor))
        runGraphGen.clicked.connect(lambda: self.runGraphGenerator(rangeNode.text(), rangeEdge.text()))

        layoutNodeEdge = QGridLayout()
        layoutNodeEdge.addWidget(rangeLabel, 0, 0)
        layoutNodeEdge.addWidget(rangeNode, 0, 1)
        layoutNodeEdge.addWidget(rangeEdgeLabel, 1, 0)
        layoutNodeEdge.addWidget(rangeEdge, 1, 1)

        layout.addLayout(layoutNodeEdge)
        layout.addWidget(runGraphGen)

        self.rightGroupBox.setLayout(layout)


    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Execution")

        runLabel = QLabel("Algorithme de d??tection de fraude :")

        radioBtn1 = QRadioButton("fBOX", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn1.setDisabled(True)
        radioBtn2 = QRadioButton("FRAUDAR", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn2.setChecked(True)
        self.algo = "fraudar"
        radioBtn3 = QRadioButton("Approche lin??aire d??terministe", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn4 = QRadioButton("Approche lin??aire stochastique", cursor=QCursor(Qt.PointingHandCursor))
        radioBtn2.toggled.connect(lambda: self.updateAlgo("fraudar"))
        radioBtn3.toggled.connect(lambda: self.updateAlgo("deterministic"))
        radioBtn4.toggled.connect(lambda: self.updateAlgo("stochastic"))

        runAlgoBtn = QPushButton("Lancer ???", cursor=QCursor(Qt.PointingHandCursor))
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


if __name__ == '__main__':

    import sys

    # Tells explicitly to OS what the correct process ID is (for displaying app logo in taskbar too)
    import ctypes
    myappid = 'fr.polytech.fraudadvisor.0.0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)
    window = FraudAdvisorUI()
    window.show()

    sys.exit(app.exec_()) 
