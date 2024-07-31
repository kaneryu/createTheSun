# stdlib imports
import sys

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import Slot as Slot
from PySide6.QtQml import  QQmlApplicationEngine
from PySide6.QtWidgets import QApplication



def main():
    app = QApplication()
    
    
    engine = QQmlApplicationEngine()

    engine.load("qml/progressbar.qml")


    sys.exit(app.exec())