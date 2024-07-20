from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QFont, QFontDatabase
import sys
import os

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
    

