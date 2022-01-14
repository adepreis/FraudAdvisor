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

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QFileDialog,
        QSlider, QStyleFactory, QTextEdit, QVBoxLayout)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.setWindowTitle("FraudAdvisor")
        self.changeStyle('Fusion')

        outputLabel = QLabel("<h2>Output</h2>")

        self.textEdit = QTextEdit() # QPlainTextEdit() ??
        self.textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n")
        self.textEdit.setReadOnly(True)
        # if new_message:
        #     self.textEdit.appendPlainText(new_message)
        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createProgressBar()

        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        outputLayout = QVBoxLayout()
        outputLayout.addWidget(outputLabel)
        outputLayout.addWidget(self.textEdit)
        topLayout = QHBoxLayout()
        topLayout.addLayout(outputLayout)
        # topLayout.addStretch(1)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.selectedDataset = ''

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        QApplication.setPalette(QApplication.style().standardPalette())

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def selectFile(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Selectionnez un dataset',
            directory=os.getcwd(),
            filter=file_filter
        )
        print(response)

        if response[0] != '':
            self.selectedDataset = response[0]
            self.textEdit.append("Vous avez sélectionné le dataset : " + self.selectedDataset)
        return response[0]

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("<h3>Dataset</h3>")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        dataLabel = QLabel("Sélectionnez le dataset\nà utiliser :")

        lineEdit = QLineEdit('')
        lineEdit.setPlaceholderText('Pas de dataset chargé')
        # lineEdit.setEchoMode(QLineEdit.Password)

        flatPushButton = QPushButton("Charger le dataset")
        flatPushButton.setFlat(True)
        flatPushButton.clicked.connect(self.selectFile)

        layout.addWidget(dataLabel)
        layout.addWidget(lineEdit)
        layout.addWidget(flatPushButton)

        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("<h3>Execution</h3>")

        runLabel = QLabel("Algorithme de détection de fraude :")

        radioButton1 = QRadioButton("fBOX")
        radioButton1.setDisabled(True)
        radioButton2 = QRadioButton("FRAUDAR")
        radioButton2.setChecked(True)
        radioButton3 = QRadioButton("Le nôtre (stochastique)")

        defaultPushButton = QPushButton("Lancer")
        defaultPushButton.setDefault(True)

        layout = QVBoxLayout()

        layout.addWidget(runLabel)
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(defaultPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 
