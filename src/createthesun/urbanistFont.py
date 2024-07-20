import os
import sys

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QLabel, QWidget


def createFonts():
    fontDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/fonts/urbanist/")
    regularId = QFontDatabase.addApplicationFont(os.path.join(fontDir, "Regular.ttf"))
    
    regular = QFontDatabase.applicationFontFamilies(regularId)

    blackId = QFontDatabase.addApplicationFont(os.path.join(fontDir, "Black.ttf"))
    black = QFontDatabase.applicationFontFamilies(blackId)

    mediumId = QFontDatabase.addApplicationFont(os.path.join(fontDir, "medium.ttf"))
    medium = QFontDatabase.applicationFontFamilies(mediumId)
    
    lightId = QFontDatabase.addApplicationFont(os.path.join(fontDir, "Light.ttf"))
    light = QFontDatabase.applicationFontFamilies(lightId)
    

