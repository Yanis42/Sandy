from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QAbstractListModel
from sandy import renameImages, getImageFiles, showErrorMessage


class ListViewModel(QAbstractListModel):
    def __init__(self, items: list[tuple[bool, str, str]]):
        super(ListViewModel, self).__init__()
        self.items = items

    def data(self, index, role):
        status, text, imgPath = self.items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return text

        if role == Qt.ItemDataRole.DecorationRole:
            if status:
                img = QPixmap(imgPath)
                img = img.scaledToHeight(64)
                return img

    def rowCount(self, index):
        return len(self.items)


class ConnectionCallbacks:
    # General

    def openSplitBtnOnUpdate(self):
        """Returns the splits file path"""
        try:
            fName = QtWidgets.QFileDialog.getOpenFileName(None, "Open Splits File", self.defaultDir, "*.lss")[0]
            self.splitPathLineEdit.setText(fName)
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    def openImagesBtnOnUpdate(self):
        """Returns the image folder path"""
        try:
            fName = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Splits Images Folder", self.defaultDir)
            self.imagesPathLineEdit.setText(fName)
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    # Simple Mode

    def renameBtnOnUpdate(self):
        """Renames the images with the given informations"""
        try:
            renameImages(
                self.debugMode,
                self.splitPathLineEdit.text(),
                self.imagesPathLineEdit.text(),
                self.imgList,
                self.similarityLineEdit.text(),
                self.pauseLineEdit.text(),
            )
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    # Advanced Mode

    def imagesPathLineEditOnUpdate(self):
        try:
            self.imgList = getImageFiles(self.imagesPathLineEdit.text())
            modelItems = [(True, imgName, f"{self.imagesPathLineEdit.text()}/{imgName}") for imgName in self.imgList]
            self.imgListView.setModel(ListViewModel(modelItems))

            # we need to set the connection there instead of the main connections init function
            model = self.imgListView.selectionModel()
            if model is not None:
                model.currentChanged.connect(self.imgListViewOnUpdate)
            else:
                raise ValueError("Model is None!")
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    def imgListViewOnUpdate(self):
        pass

    # Settings

    def similarityCheckBoxOnUpdate(self):
        pass

    def pauseCheckBoxOnUpdate(self):
        pass

    def delayCheckBoxOnUpdate(self):
        pass

    def comparisonCheckBoxOnUpdate(self):
        pass

    def loopCheckBoxOnUpdate(self):
        pass

    def similarityValueOnUpdate(self):
        pass

    def pauseValueOnUpdate(self):
        pass

    def delayValueOnUpdate(self):
        pass

    def comparisonComboBoxOnUpdate(self):
        pass

    def loopValueOnUpdate(self):
        pass

    # Flags

    def dummyFlagCheckBoxOnUpdate(self):
        pass

    def belowFlagCheckBoxOnUpdate(self):
        pass

    def pauseFlagCheckBoxOnUpdate(self):
        pass

    # Export

    def exportFolderBtnOnUpdate(self):
        try:
            fName = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Export Folder", self.defaultDir)
            self.exportPathLineEdit.setText(fName)
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    def exportBtnOnUpdate(self):
        pass
