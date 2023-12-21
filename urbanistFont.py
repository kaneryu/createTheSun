from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont, QFontDatabase
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
    
    print(regular)
    print(black)
    print(medium)

