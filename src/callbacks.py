from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QAbstractListModel
from sandy import renameImages, getImageFiles, showErrorMessage
from data import SplitProperties, SplitSettings


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

            if len(self.imgList) == 0:
                raise RuntimeError("No image were found in this folder.")

            modelItems = [(True, imgName, f"{self.imagesPathLineEdit.text()}/{imgName}") for imgName in self.imgList]
            self.imgListView.setModel(ListViewModel(modelItems))

            # we need to set the connection there instead of the main connections init function
            model = self.imgListView.selectionModel()
            if model is not None:
                model.currentChanged.connect(self.imgListViewOnUpdate)
            else:
                raise ValueError("Model is None!")

            # init parameters for found images
            if self.splitPropertyList is None:
                self.splitPropertyList = []
                dummyIdx = belowIdx = pauseIdx = 0
                for img in self.imgList:
                    # parse name's elements
                    imgElems = img.split("_")
                    name = imgElems[1] if "dummy" not in img else f"{imgElems[1]}_{imgElems[2]}"
                    name = name.removesuffix(".png")
                    splitProperties = SplitProperties(int(imgElems[0]), name, SplitSettings())

                    settings = splitProperties.settings
                    for elem in imgElems:
                        elem = elem.removesuffix(".png")

                        if elem.startswith("(") and elem.endswith(")"):
                            settings.similarity.setSetting(splitProperties.name, "(,)", float(elem[1:][:-1]))

                        if elem.startswith("[") and elem.endswith("]"):
                            settings.pauseTime.setSetting(splitProperties.name, "[,]", float(elem[1:][:-1]))

                        if elem.startswith("#") and elem.endswith("#"):
                            settings.delayTime.setSetting(splitProperties.name, "#,#", float(elem[1:][:-1]))

                        if elem.startswith("^") and elem.endswith("^"):
                            settings.comparisonMethod.setSetting(splitProperties.name, "^,^", float(elem[1:][:-1]))

                        if elem.startswith("@") and elem.endswith("@"):
                            settings.imgLoop.setSetting(splitProperties.name, "@,@", float(elem[1:][:-1]))

                        if elem.startswith("{") and elem.endswith("}"):
                            if "d" in elem:
                                dummyIdx += 1
                                settings.flags.dummy.setFlag(dummyIdx, splitProperties.name, "d")

                            if "b" in elem:
                                belowIdx += 1
                                settings.flags.below.setFlag(belowIdx, splitProperties.name, "b")

                            if "p" in elem:
                                pauseIdx += 1
                                settings.flags.pause.setFlag(pauseIdx, splitProperties.name, "p")

                    self.splitPropertyList.append(splitProperties)
                self.activeSplitProperties = self.splitPropertyList[0]
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

    def imgListViewOnUpdate(self):
        try:
            self.activeProps: SplitProperties = self.splitPropertyList[self.imgListView.currentIndex().row()]
            settings = self.activeProps.settings

            state = Qt.CheckState.Checked if settings.similarity.isEnabled else Qt.CheckState.Unchecked
            self.similarityCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.pauseTime.isEnabled else Qt.CheckState.Unchecked
            self.pauseCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.delayTime.isEnabled else Qt.CheckState.Unchecked
            self.delayCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.comparisonMethod.isEnabled else Qt.CheckState.Unchecked
            self.comparisonCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.imgLoop.isEnabled else Qt.CheckState.Unchecked
            self.loopCheckBox.setCheckState(state)

            self.similarityValue.setValue(settings.similarity.value)
            self.pauseValue.setValue(int(settings.pauseTime.value))
            self.delayValue.setValue(int(settings.delayTime.value))
            self.comparisonComboBox.setCurrentIndex(int(settings.comparisonMethod.value))
            self.loopValue.setValue(int(settings.imgLoop.value))

            state = Qt.CheckState.Checked if settings.flags.dummy.isEnabled else Qt.CheckState.Unchecked
            self.dummyFlagCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.flags.below.isEnabled else Qt.CheckState.Unchecked
            self.belowFlagCheckBox.setCheckState(state)

            state = Qt.CheckState.Checked if settings.flags.pause.isEnabled else Qt.CheckState.Unchecked
            self.pauseFlagCheckBox.setCheckState(state)
        except Exception as e:
            showErrorMessage(self, f"An error occurred: {e}")

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
