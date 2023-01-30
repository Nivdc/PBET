import sys
from pathlib import Path
from shutil import copyfile

from toc2csv import toc2csv
from csv2toc import csv2toc
from textshot import Snipper

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QApplication, QLineEdit, QAction, 
                        QFileDialog, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                        QLabel, QDockWidget, QCheckBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt

import pytesseract

gFileName = None
gLoadVC = False
gTextEdit = None
gMainWindow = None

def main():

    app = QApplication(sys.argv)

    w = QMainWindow()
    global gMainWindow
    gMainWindow = w             # For ocrCallback. So complicated :<

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
    poqle.setText("0")
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
    cb.stateChanged.connect(lambda:switchLoadVC())

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
    w.statusBar().showMessage('Ready.')

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
        global gFileName
        gFileName = fname[0]
        mainWindow.statusBar().showMessage("File selected.")
    elif fname[0]:
        pathqle.setText(fname[0])
        mainWindow.statusBar().showMessage("ERROR: This is not a pdf file.")

def loadBookmark(textEdit, delimqle):
    if gFileName and gFileName[-4:].lower() == ".pdf":
        textEdit.append(toc2csv(gFileName, delimqle.text(), 'r', gLoadVC))

def ocr(mainWindow, ocrlangqle):
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        print(
            "INFO: Tesseract is either not installed or cannot be reached.\n"
            "Please select tesseract.exe, see README file for more information."
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
    if reslut != None:
        gTextEdit.append(reslut)
    else:
        gMainWindow.statusBar().showMessage("Unable to read text from image, try again ?")

def save(mainWindow, textEdit, poqle, delimqle):
    try:
        newFileName = createNewFile(gFileName)
        try:
            po = int(poqle.text())
        except:
            po = 0

        csv2toc(textEdit.toPlainText(), newFileName, delimqle.text(), po)
    except Exception as e:
        mainWindow.statusBar().showMessage("ERROR: "+str(e))
    else:
        mainWindow.statusBar().showMessage(f"Saved successfully, The new file name is '{Path(newFileName).name}'.")

def createNewFile(srcFileName):
    newFileName = srcFileName[:-4] + "-new.pdf"
    copyfile(srcFileName, newFileName)
    return newFileName

def switchLoadVC():
    global gLoadVC
    gLoadVC = not gLoadVC

if __name__ == '__main__':
    main()