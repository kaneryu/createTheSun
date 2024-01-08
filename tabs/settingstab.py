#standard imports
import json
#third party imports
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpacerItem, QFrame, QGridLayout
from PyQt6.QtGui import QIntValidator
#local imports
import save


def save_():
    save.save()
def load():
    save.load()
settings = {
    
    "save": {
        "name": "Save",
        "description": "Save your progress",
        "action": save_,
        "buttonName": "Save"
    },
    "load": {
        "name": "Load",
        "description": "Load your progress",
        "action": load,
        "buttonName": "Load"
    },
    
    
    
}

class setting(QFrame):
    def __init__(self, setting):
        super().__init__()
        self.thing = setting
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout_ = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        
        self.label = QLabel(settings[setting]["name"])
        self.label.setWordWrap(True)
        self.setToolTip(settings[setting]["description"])
        self.setToolTipDuration(5000)
        self.layout_.addWidget(self.label, 0, 0)
        
        self.button = QPushButton(settings[setting]["buttonName"])
        self.button.clicked.connect(settings[setting]["action"])
        self.layout_.addWidget(self.button, 0, 1)
        
        self.setLayout(self.layout_)


class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_)
        
        widgets = []
        for i in settings:
            widgets.append(setting(i))
            self.layout_.addWidget(widgets[-1])
        

    