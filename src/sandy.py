from xml.etree import ElementTree as ET
from os import walk, rename
from PIL import Image


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
    for (dirPath, dirNames, fileNames) in walk(imgDirPath):
        files.extend(fileNames)

    # make sure we keep PNGs
    for file in files:
        if ".png" not in file:
            files.remove(file)

    return files


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


def hasImageTransparency(imgFilePath: str):
    """Checks if the given image has transparency or not"""
    # https://stackoverflow.com/a/58567453

    img = Image.open(imgFilePath)

    if img.info.get("transparency", None) is not None:
        return True

    if img.mode == "P":
        transparent = img.info.get("transparency", -1)

        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        if img.getextrema()[3][0] < 255:
            return True

    return False


def renameImages(xmlPath: str, imgDirPath: str, similarity: str, pauseTime: str):
    """Changes every image filenames to the AutoSplit format"""
    lssRoot = getRoot(xmlPath)

    if lssRoot is not None:
        imgNames = getImageFiles(imgDirPath)
        splitNames = getSplitNames(lssRoot)
        lastName = splitNames.pop(0)
        dummyIdx = 0
        index = 1

        for i, imgName in enumerate(imgNames, 0):
            # get current image's path
            imgPath = f"{imgDirPath}/{imgName}"

            # create the flag list
            maskFlag = "m" if hasImageTransparency(imgPath) else ""
            dummyFlag = "d" if "dummy" in imgName else ""
            flags = ("_{" + f"{maskFlag}{dummyFlag}" + "}") if maskFlag != "" or dummyFlag != "" else ""

            # only update the name and split number if the previous split is a real split
            if i > 0 and "dummy" not in imgNames[i - 1]:
                index += 1
                lastName = splitNames.pop(0)

            splitName = lastName
            if "dummy" in imgName:
                # add the dummy number to the name if the current image is a dummy
                dummyIdx += 1
                splitName = f"d{dummyIdx}{lastName}"

            # create the new filename and rename the current file
            newName = f"{index:03}_{splitName}_({similarity})_[{pauseTime}]{flags}.png"
            rename(imgPath, f"{imgDirPath}/{newName}")
