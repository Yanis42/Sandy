from xml.etree import ElementTree as ET
from os import walk, rename
from data import SplitProperties, SplitSettings


def getRoot(xmlPath: str):
    """Try to parse an XML file, opens an 'Open File Dialog' if file not found"""
    # .LSS files uses the XML format

    try:
        root = ET.parse(xmlPath).getroot()
    except FileNotFoundError:
        root = None

    return root


def getImageFiles(imgDirPath: str):
    """Returns the list of images filenames inside the image folder"""
    files: list[str] = []

    # get every filenames inside the folder
    for dirPath, dirNames, fileNames in walk(imgDirPath):
        files.extend(fileNames)

    # make sure we keep PNGs
    for file in files:
        if ".png" not in file:
            files.remove(file)

    # at this point names with "dummy" comes after the real split, which is not what we want
    sortedFiles = []
    for i, file in enumerate(sorted(files)):
        sortedFiles.append(file)
        if i > 0 and "dummy" in file:
            sortedFiles.remove(file)
            sortedFiles.insert(i - 1, file)

    return sortedFiles


def getSplitNames(lssRoot: ET.Element):
    """Returns the split names from the given .LSS file"""
    names: list[str] = []

    if lssRoot is not None:
        for segments in lssRoot.iterfind("Segments"):
            for segment in segments:
                for name in segment.iterfind("Name"):
                    if name.text is not None:
                        names.append(name.text.replace(" ", ""))

    return names


def renameImages(isDebugMode: bool, xmlPath: str, imgDirPath: str, similarity: str, pauseTime: str):
    """Changes every image filenames to the AutoSplit format"""
    lssRoot = getRoot(xmlPath)

    if lssRoot is not None:
        imgNames = getImageFiles(imgDirPath)
        splitNames = getSplitNames(lssRoot)
        lastName = splitNames.pop(0)
        dummyIdx = 0
        index = 1

        for i, imgName in enumerate(imgNames, 0):
            # init split settings
            splitSettings = SplitSettings()

            # only update the name and split number if the previous split is a real split
            if i > 0 and "dummy" not in imgNames[i - 1]:
                index += 1
                lastName = splitNames.pop(0)
            splitName = lastName

            # create the flag list and add the dummy number to the name if the current image is a dummy
            if "dummy" in imgName:
                dummyIdx += 1
                splitSettings.flags.dummy.setFlag(dummyIdx, lastName, "d")
                splitName = splitSettings.flags.dummy.getName()  # returns the split name if not enabled

            splitSettings.similarity.setSetting(splitName, "(,)", float(similarity))
            splitSettings.pauseTime.setSetting(splitName, "[,]", float(pauseTime))

            # create the new filename and rename the current file
            newName = SplitProperties(index, splitName, splitSettings).getSplitName()

            oldPath = f"{imgDirPath}/{imgName}"
            newPath = f"{imgDirPath}/{newName}"
            if isDebugMode:
                print(f"Old Path: `{oldPath}`, New Path: `{newPath}`")
            else:
                rename(oldPath, newPath)
