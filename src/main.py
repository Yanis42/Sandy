#!/usr/bin/env python3

from PyQt6 import QtWidgets
from PyQt6.uic import load_ui
from pathlib import Path
from sys import exit, argv
from os import path
from argparse import ArgumentParser as Parser
from callbacks import ConnectionCallbacks


class MainWindow(QtWidgets.QMainWindow, ConnectionCallbacks):
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
        self.imgList = None
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

    # --- Connection Callbacks ---#

    def initConnections(self):
        """Initialises the callbacks"""

        # General
        self.openSplitBtn.clicked.connect(self.openSplitBtnOnUpdate)
        self.openImagesBtn.clicked.connect(self.openImagesBtnOnUpdate)

        # Simple Mode
        self.renameBtn.clicked.connect(self.renameBtnOnUpdate)

        # Advanced Mode
        self.imagesPathLineEdit.textChanged.connect(self.imagesPathLineEditOnUpdate)

        self.similarityCheckBox.stateChanged.connect(self.similarityCheckBoxOnUpdate)
        self.pauseCheckBox.stateChanged.connect(self.pauseCheckBoxOnUpdate)
        self.delayCheckBox.stateChanged.connect(self.delayCheckBoxOnUpdate)
        self.comparisonCheckBox.stateChanged.connect(self.comparisonCheckBoxOnUpdate)
        self.loopCheckBox.stateChanged.connect(self.loopCheckBoxOnUpdate)

        self.similarityValue.valueChanged.connect(self.similarityValueOnUpdate)
        self.pauseValue.valueChanged.connect(self.pauseValueOnUpdate)
        self.delayValue.valueChanged.connect(self.delayValueOnUpdate)
        self.comparisonComboBox.currentTextChanged.connect(self.comparisonComboBoxOnUpdate)
        self.loopValue.valueChanged.connect(self.loopValueOnUpdate)

        self.dummyFlagCheckBox.stateChanged.connect(self.dummyFlagCheckBoxOnUpdate)
        self.belowFlagCheckBox.stateChanged.connect(self.belowFlagCheckBoxOnUpdate)
        self.pauseFlagCheckBox.stateChanged.connect(self.pauseFlagCheckBoxOnUpdate)

        self.exportFolderBtn.clicked.connect(self.exportFolderBtnOnUpdate)
        self.exportBtn.clicked.connect(self.exportBtnOnUpdate)


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
