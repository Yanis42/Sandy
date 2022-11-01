#!/usr/bin/env python3

from PyQt6 import QtWidgets
from PyQt6.uic import load_ui
from pathlib import Path
from sys import exit, argv
from os import path, name as osName
from sandy import renameImages


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """Main initialisation function"""
        super(MainWindow, self).__init__()
        load_ui.loadUi((path.dirname(path.abspath(__file__)) + "/../res/MainWindow.ui"), self)
        self.defaultDir = str(Path.home())
        self.initConnections()

    # connections callbacks

    def openSplitFile(self):
        """Returns the splits file path"""
        try:
            fName = QtWidgets.QFileDialog.getOpenFileName(None, "Open Splits File", self.defaultDir, "*.lss")[0]
            self.splitPathLineEdit.setText(fName)
        except:
            pass

    def openImagesFolder(self):
        """Returns the image folder path"""
        try:
            fName = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Splits Images Folder", self.defaultDir)
            self.imagesPathLineEdit.setText(fName)
        except:
            pass

    def executeRename(self):
        """Renames the images with the given informations"""
        renameImages(
            self.splitPathLineEdit.text(),
            self.imagesPathLineEdit.text(),
            self.similarityLineEdit.text(),
            self.pauseLineEdit.text(),
        )

    def initConnections(self):
        """Initialises the callbacks"""
        self.openSplitBtn.clicked.connect(self.openSplitFile)
        self.openImagesBtn.clicked.connect(self.openImagesFolder)
        self.renameBtn.clicked.connect(self.executeRename)


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()

    try:
        from qdarktheme import load_stylesheet

        app.setStyleSheet(load_stylesheet())
    except ModuleNotFoundError:
        pass

    mainWindow.show()
    exit(app.exec())
