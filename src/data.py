from dataclasses import dataclass


@dataclass
class SplitFlagElement:
    index: int
    splitName: str
    outputName: str
    isEnabled: bool = False

    def setFlag(self, index: int, splitName: str, outputName: str = "", isEnabled: bool = True):
        self.index = index
        self.splitName = splitName
        self.outputName = outputName
        self.isEnabled = isEnabled

    def getName(self):
        """Returns a string based on the parameters we set, only used for dummy flags"""
        return f"{self.outputName}{self.index}{self.splitName}" if self.isEnabled else f"{self.splitName}"


@dataclass
class SplitFlagSettings:
    dummy = SplitFlagElement(0, "", "")
    below = SplitFlagElement(0, "", "")
    pause = SplitFlagElement(0, "", "")
    isEnabled: bool = True

    def getFlags(self):
        flags = []

        if self.isEnabled:
            if self.dummy is not None and self.dummy.isEnabled:
                flags.append("d")

            if self.below is not None and self.below.isEnabled:
                flags.append("b")

            if self.pause is not None and self.pause.isEnabled:
                flags.append("p")

        return "{" + "".join(flag for flag in flags) + "}" if len(flags) > 0 else ""


@dataclass
class SplitSettingElement:
    splitName: str
    tag: str
    value: float
    isEnabled: bool = False

    valMin: float = None
    valMax: float = None

    def setSetting(self, splitName: str = "", tag: str = "", value: float = 0.0, isEnabled: bool = True):
        self.splitName = splitName
        self.tag = tag
        self.value = value
        self.isEnabled = isEnabled

    def getSetting(self):
        if (self.valMin is None and self.valMax is None) or (self.value >= self.valMin and self.value <= self.valMax):
            return f"{self.tag.split(',')[0]}{self.value}{self.tag.split(',')[1]}"  # i.e.: ``(0.95)``
        else:
            raise ValueError(
                f"ERROR: The threshold value for Split `{self.splitName}` isn't between "
                + f"{self.valMin} and {self.valMax}. Value: {self.value}"
            )


@dataclass
class SplitSettings:
    similarity = SplitSettingElement("", "", 0.0, valMin=0.0, valMax=1.0)
    pauseTime = SplitSettingElement("", "", 0.0)
    delayTime = SplitSettingElement("", "", 0.0)
    comparisonMethod: SplitSettingElement = SplitSettingElement("", "", 0.0)
    imgLoop = SplitSettingElement("", "", 0.0)
    flags = SplitFlagSettings()

    def getSettings(self):
        settings = []

        if self.similarity is not None and self.similarity.isEnabled:
            settings.append(self.similarity.getSetting())

        if self.pauseTime is not None and self.pauseTime.isEnabled:
            settings.append(self.pauseTime.getSetting())

        if self.delayTime is not None and self.delayTime.isEnabled:
            settings.append(self.delayTime.getSetting())

        if self.comparisonMethod is not None and self.comparisonMethod.isEnabled:
            settings.append(self.comparisonMethod.getSetting())

        if self.imgLoop is not None and self.imgLoop.isEnabled:
            settings.append(self.imgLoop.getSetting())

        if self.flags is not None and self.flags.isEnabled:
            settings.append(self.flags.getFlags())

        return "_".join(setting for setting in settings if len(setting) > 0) if len(settings) > 0 else ""


@dataclass
class SplitProperties:
    index: int
    name: str
    settings: SplitSettings

    def getSplitName(self):
        return f"{self.index:03}_{self.name}_" + self.settings.getSettings() + ".png"
