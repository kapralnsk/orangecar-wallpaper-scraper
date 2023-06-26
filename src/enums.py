from enum import Enum


class ImagesetTypes(Enum):
    DESKTOP = "dlDesktopImg"
    TABLET = "dlTabletImg"
    THUMBNAIL = "dlThumbnailImg"


class ImagesetSizes(Enum):
    LARGE = "large"
    SMALLSQUARE = "smallsquare"
    MEDIUMSQUARE = "mediumsquare"
    LARGESQUARE = "largesquare"
    SMALL = "small"
    THUMBNAIL = "thumbnail"
    ORIGINAL = "original"


class Teams(Enum):
    FORMULA_E = "formulaE"
    EXTREME_E = "extremeE"
    F1 = "f1"
