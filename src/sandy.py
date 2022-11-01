from multiprocessing import dummy
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
    files: list[str] = []

    for (dirPath, dirNames, fileNames) in walk(imgDirPath):
        files.extend(fileNames)

    return files


def getSplitNames(lssRoot: ET.Element):
    names: list[str] = []

    if lssRoot is not None:
        for segments in lssRoot.iterfind("Segments"):
            for segment in segments:
                for name in segment.iterfind("Name"):
                    if name.text is not None:
                        names.append(name.text.replace(" ", ""))

    return names


def hasImageTransparency(imgFilePath: str):
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
    lssRoot = getRoot(xmlPath)

    if lssRoot is not None:
        imgPaths = getImageFiles(imgDirPath)
        splitNames = getSplitNames(lssRoot)
        lastName = splitNames.pop(0)
        dummyIdx = 0
        index = 1

        for i, imgName in enumerate(imgPaths, 0):
            imgPath = f"{imgDirPath}/{imgName}"
            maskTag = f"m" if hasImageTransparency(imgPath) else ""
            dummyTag = f"d" if "dummy" in imgName else ""
            flags = ("_{" + f"{maskTag}{dummyTag}" + "}") if maskTag != "" or dummyTag != "" else ""

            # only update the name if the previous split is a real split
            if i > 0 and "dummy" not in imgPaths[i - 1]:
                index += 1
                lastName = splitNames.pop(0)

            if "dummy" in imgPath:
                dummyIdx += 1
                splitName = f"d{dummyIdx}{lastName}"
            else:
                splitName = lastName

            newName = f"{index:03}_{splitName}_({similarity})_[{pauseTime}]{flags}.png"

            try:
                rename(imgPath, f"{imgDirPath}/{newName}")
            except FileExistsError:
                rename(imgPath, f"{imgDirPath}/{newName.replace('.png', 'REMOVE_ME.png')}")
