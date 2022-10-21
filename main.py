import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QApplication, QLineEdit, QAction, 
                        QFileDialog, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                        QLabel, QDockWidget, QCheckBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
from pathlib import Path

from toc2csv import toc2csv
from csv2toc import csv2toc

from textshot import Snipper
import pytesseract

fileName = None
loadVC = False
gTextEdit = None

def main():

    app = QApplication(sys.argv)
    w = QMainWindow()

    textEdit = QTextEdit()
    textEdit.setFontPointSize(12)
    global gTextEdit
    gTextEdit = textEdit        # For ocrCallback. So complicated :<

    pathqle = QLineEdit(w)
    pathqle.setReadOnly(True)
    pathqle.setPlaceholderText("Please select a file.")

    selectFile = QAction('Select', w)
    selectFile.triggered.connect(lambda:fileDialog(w, pathqle))

    polb = QLabel('Page Offset:', w)
    poqle = QLineEdit(w)
    poqle.setPlaceholderText("0")
    pohbox = QHBoxLayout()
    pohbox.addWidget(polb)
    pohbox.addWidget(poqle)

    delimlb = QLabel('CSV delimiter:', w)
    delimqle = QLineEdit(w)
    delimqle.setText("~")
    delimqle.setMaxLength(1)
    delimhbox = QHBoxLayout()
    delimhbox.addWidget(delimlb)
    delimhbox.addWidget(delimqle)

    loadBtn = QPushButton('LoadBookmark')
    loadBtn.clicked.connect(lambda:loadBookmark(textEdit, delimqle))

    cb = QCheckBox('loadWithVCoord', w)
    cb.stateChanged.connect(lambda:SwitchLoadVC())

    ocrlanglb = QLabel('OCR lang:', w)
    ocrlangqle = QLineEdit(w)
    ocrlangqle.setText("eng")
    ocrlanghbox = QHBoxLayout()
    ocrlanghbox.addWidget(ocrlanglb)
    ocrlanghbox.addWidget(ocrlangqle)

    ocrBtn = QPushButton('OCR')
    ocrBtn.clicked.connect(lambda:ocr(w, ocrlangqle))

    saveBtn = QPushButton('Save')
    saveBtn.clicked.connect(lambda:save(w, textEdit, poqle, delimqle))

    vbox = QVBoxLayout()
    vbox.addLayout(pohbox)
    vbox.addLayout(delimhbox)
    vbox.addWidget(loadBtn)
    vbox.addWidget(cb)
    vbox.addWidget(ocrBtn)
    vbox.addLayout(ocrlanghbox)
    vbox.addStretch(1)          # This doesn't work...I don't know why :<
    vbox.addWidget(saveBtn)

    rightBar = QWidget()
    rightBar.setLayout(vbox)

    dock = QDockWidget() 
    dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

    w.setMinimumSize(600, 400)
    w.setWindowTitle('PDFBookMarkII')
    w.setCentralWidget(textEdit)
    w.statusBar().showMessage('File not loaded.')

    tb = w.addToolBar("SelectFile")
    tb.addWidget(pathqle)
    tb.addAction(selectFile)

    w.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
    dock.setTitleBarWidget(rightBar)

    w.show()
    sys.exit(app.exec())

def fileDialog(mainWindow,pathqle):
    home_dir = str(Path.home())
    fname = QFileDialog.getOpenFileName(mainWindow, 'Open file', home_dir, "PDFs (*.pdf *.PDF)")

    if fname[0] and fname[0][-4:].lower() == ".pdf":
        pathqle.setText(fname[0])
        global fileName
        fileName = fname[0]
        mainWindow.statusBar().showMessage("File opened.")
    elif fname[0]:
        pathqle.setText(fname[0])
        mainWindow.statusBar().showMessage("This isn't a pdf file.")

def loadBookmark(textEdit, delimqle):
    if fileName and fileName[-4:].lower() == ".pdf":
        textEdit.setText(toc2csv(fileName, delimqle.text(), 'r', loadVC))

def ocr(mainWindow, ocrlangqle):
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        print(
            "INFO: Tesseract is either not installed or cannot be reached.\n"
            "See README file for more information."
        )
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(mainWindow, 'Select tesseract.exe', home_dir, "exec (*.exe)")
        if fname[0] and fname[0][-4:].lower() == ".exe":
            setTesseractPath(fname[0])

    else:
        s = Snipper(mainWindow)
        s.callback = ocrCallback
        s.lang = ocrlangqle.text()
        s.show()

def setTesseractPath(tpath):
    pytesseract.pytesseract.tesseract_cmd = tpath
    pyt_file_path = Path(str(Path(pytesseract.__file__).parent) + "/pytesseract.py")

    #read
    with open(pyt_file_path, mode='r') as pyt_file:
        buf = pyt_file.readlines()

    #replace
    for idx, line in enumerate(buf):
        if line.startswith("tesseract_cmd ="):
            buf[idx] = f"tesseract_cmd = r'{tpath}'\n"
            break

    #rewrite
    with open(pyt_file_path, mode='w') as pyt_file:
        pyt_file.writelines(buf)

def ocrCallback(reslut):
    gTextEdit.append(reslut)

def save(mainWindow, textEdit, poqle, delimqle):
    try:
        try:
            po = int(poqle.text())
        except:
            po = 0

        csv2toc(textEdit.toPlainText(), fileName, delimqle.text(), po)
    except Exception as e:
        mainWindow.statusBar().showMessage("Error: "+str(e))
    else:
        mainWindow.statusBar().showMessage("Saved successfully")

def SwitchLoadVC():
    global loadVC
    loadVC = not loadVC

if __name__ == '__main__':
    main()