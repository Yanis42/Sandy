#!/usr/bin/env python3

from PyQt6 import QtWidgets
from PyQt6.uic import load_ui
from pathlib import Path
from sys import exit, argv
from os import path
from argparse import ArgumentParser as Parser
from sandy import renameImages


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """Main initialisation function"""
        super(MainWindow, self).__init__()

        args = self.getArguments()
        self.debugMode = args.debug

        uiPath = path.dirname(path.abspath(__file__)) + "/../res/MainWindow.ui"
        if not path.isfile(uiPath):
            # temp fix for executables
            uiPath = uiPath.replace("/..", "")
        load_ui.loadUi(uiPath, self)

        self.defaultDir = str(Path.home())
        self.initConnections()

    def getArguments(self):
        """Initialisation of the argument parser"""

        parser = Parser(description="Fix various things related to assets for the OoT Decomp")

        parser.add_argument(
            "-d",
            "--debug",
            dest="debug",
            default=False,
            action="store_true",
            help="Enable debug mode. This will print the file names instead of renaming them.",
        )

        return parser.parse_args()

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
            self.debugMode,
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
