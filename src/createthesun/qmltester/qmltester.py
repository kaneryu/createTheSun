# stdlib imports
import sys

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import Slot as Slot
from PySide6.QtQml import  QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QHBoxLayout, QWidget


class App(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.setWindowTitle("QML tester")
        
        self.reloadButton = QPushButton("Reload")
        self.reloadButton.clicked.connect(self.reload)
        
        self.urlInput = QLineEdit()
        self.urlInput.setPlaceholderText("Enter URL")
        
        self.engine = engine
        
        self.container = QWidget()
        self.layout_ = QHBoxLayout()
        
        self.container.setLayout(self.layout_)
        self.setCentralWidget(self.container)
        
        self.layout_.addWidget(self.urlInput)
        self.layout_.addWidget(self.reloadButton)
    
    def reload(self):
        
        self.engine.load(self.urlInput.text())
        

def main():
    app = QApplication()
    
    
    engine = QQmlApplicationEngine()

    otherApp = App(engine)
    otherApp.show()


    sys.exit(app.exec())

main()