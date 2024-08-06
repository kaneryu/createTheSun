# stdlib imports
import dataclasses
import enum
import os
import random
import sys
import threading
import time

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, Qt, QTimer
from PySide6.QtCore import Signal as QSignal
from PySide6.QtCore import Slot as Slot, QDir
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtQml import (
    QmlElement,
    QmlSingleton,
    QQmlApplicationEngine,
    qmlRegisterSingletonInstance,
    qmlRegisterSingletonType,
)
from PySide6.QtWidgets import QApplication

# local imports
from . import materialInterface, urbanistFont, gamedefine, iLoveModelsTotally, itemInteractions



    

@dataclasses.dataclass
class Tab:
    name: str = ""
    internalName: str = ""
    
QML_IMPORT_NAME = "CreateTheSun"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0

class Items(QObject):
    def __init__(self):
        super().__init__()
        for i in gamedefine.items:
            setattr(self, i.lower(), gamedefine.items[i])
    
    @Slot(str, result=QObject)
    def getItem(self, name: str):
        return getattr(self, name.lower())
    
@QmlElement
class Backend(QObject):
    loadComplete = QSignal(name="loadComplete")
    activeTabChanged = QSignal(name="activeTabChanged")
    # tabModelChanged = QSignal(name="tabModelChanged")
    _instance = None
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._value = 0
            
        self._activeTab = "mainTab"   
        
    @Property(str, notify=activeTabChanged)
    def activeTab(self):
        return self._activeTab
    
    @activeTab.setter
    def activeTab(self, value):
        self._activeTab = value
        self.activeTabChanged.emit()
    
    

def findQmlFile() -> str | None:
    # Find the QML file
    for path in [os.path.join(os.path.dirname(__file__), 'qml'), os.path.join(os.path.dirname(__file__))]:
        for file in os.listdir(path):
            if file == 'main~2x3x.qml':
                return os.path.join(path, file)
    return None
 
def createTabModel():
    model = iLoveModelsTotally.ListModel(contains=Tab)
    model.addItem(Tab(name = "Stats", internalName = "stats"))
    model.addItem(Tab("Save & Load", internalName = "saveLoad"))
    model.addItem(Tab("Goals", internalName = "goals"))
    model.addItem(Tab("Achevements", internalName = "achevements"))
    model.addItem(Tab("Automation", internalName = "automation"))
    model.addItem(Tab("Main Tab", internalName = "mainTab"))
    return model

def generateRandomHexColor():
    return random.randint(0, 0xFFFFFF)

@dataclasses.dataclass
class Item:
    item: QObject = None
    
def createItemModel():      
    ItemsModel = iLoveModelsTotally.ListModel(contains=Item)
    for i in gamedefine.items:
        ItemsModel.addItem(Item(item=gamedefine.items[i]))
        
    return ItemsModel
    

def main():
    app = QApplication()
    
    fonts = urbanistFont.createFonts()
    app.setFont(QFont(fonts[0][0]))
    
    
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    qml = findQmlFile()

    backend = Backend()

    theme = materialInterface.Theme()
    theme.get_dynamicColors(0x18130B, True, 0.0)
    items = Items()

    
    if not qml:
        print('Could not find QML file')
        sys.exit(1)
    else:
        engine.load(qml)
    
    engine.rootContext().setContextProperty("Theme", theme)
    engine.rootContext().setContextProperty("Backend", backend)
    engine.rootContext().setContextProperty("Items", items)
    
    tabsModel = createTabModel()

    engine.rootObjects()[0].setProperty("tabsModel", tabsModel)
    
    ItemsModel = createItemModel()
    engine.rootContext().setContextProperty("ItemsModel", ItemsModel)
    
    # tim = QTimer()
    # tim.setInterval(1000)
    # tim.timeout.connect(lambda: theme.get_dynamicColors(generateRandomHexColor(), True, 0.0))
    # tim.start()
    
    
    print(QDir.currentPath())
    time.sleep(0.3)
    # Main Theme Source Color: #DCAB5C
    backend.loadComplete.emit()
    engine.rootObjects()[0].show()
    sys.exit(app.exec())