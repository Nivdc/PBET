import sys
from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QApplication, QLineEdit, 
                        QFileDialog, QWidget, QVBoxLayout, QPushButton, QDockWidget, QCheckBox)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from pathlib import Path

from toc2csv import toc2csv
from csv2toc import csv2toc

fileName = None
loadVC = False

def main():

    app = QApplication(sys.argv)
    textEdit = QTextEdit()
    w = QMainWindow()

    pathqle = QLineEdit(w)
    pathqle.setReadOnly(True)
    pathqle.setPlaceholderText("Please select a file.")

    poqle = QLineEdit(w)
    poqle.setPlaceholderText("Page Offset.")

    selectFile = QAction('Select', w)
    selectFile.triggered.connect(lambda:fileDialog(w, pathqle))

    loadBtn = QPushButton('LoadBookmark')
    loadBtn.clicked.connect(lambda:loadBookmark(textEdit))

    saveBtn = QPushButton('Save')
    saveBtn.clicked.connect(lambda:save(w, textEdit, poqle))

    cb = QCheckBox('loadWithVCoord', w)
    cb.stateChanged.connect(lambda:SwitchLoadVC())

    vbox = QVBoxLayout()
    vbox.addWidget(loadBtn)
    vbox.addWidget(cb)
    vbox.addSpacing(250)
    vbox.addWidget(saveBtn)


    buttonBar = QWidget()
    buttonBar.setLayout(vbox)

    dock = QDockWidget() 
    dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

    w.setFixedSize(512, 384)
    w.setWindowTitle('PDFBookMarkII')
    w.setCentralWidget(textEdit)
    w.statusBar().showMessage('File not loaded.')

    tb = w.addToolBar("SelectFile")
    tb.addWidget(pathqle)
    tb.addWidget(poqle)
    tb.addAction(selectFile)

    w.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
    dock.setTitleBarWidget(buttonBar)

    w.show()
    sys.exit(app.exec())

def fileDialog(w,pathqle):
    home_dir = str(Path.home())
    fname = QFileDialog.getOpenFileName(w, 'Open file', home_dir)

    if fname[0] and fname[0][-4:].lower() == ".pdf":
        pathqle.setText(fname[0])
        global fileName
        fileName = fname[0]
        w.statusBar().showMessage("File opened.")
    else:
        pathqle.setText(fname[0])
        w.statusBar().showMessage("This is not a pdf file.")

def loadBookmark(textEdit):
    if fileName and fileName[-4:].lower() == ".pdf":
        textEdit.setText(toc2csv(fileName,';','r', loadVC))

def save(w, textEdit, poqle):
    try:
        try:
            po = int(poqle.text())
        except:
            po = 0

        csv2toc(textEdit.toPlainText(), fileName, ';', po)
    except Exception as e:
        w.statusBar().showMessage("Error: "+str(e))
    else:
        w.statusBar().showMessage("Saved successfully")

def SwitchLoadVC():
    global loadVC
    loadVC = not loadVC

if __name__ == '__main__':
    main()