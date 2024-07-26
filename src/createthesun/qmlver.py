# stdlib imports
import dataclasses
import enum
import os
import random
import sys
import threading

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, Qt, QTimer
from PySide6.QtCore import Signal as QSignal
from PySide6.QtCore import Slot as Slot
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
from . import materialInterface, urbanistFont


@dataclasses.dataclass
class Item:
    thing: str = ""
    things: str = ""
    objects: str = ""
    multi: str = ""
    
class ListModel(QAbstractListModel):
    def __init__(self, contains = Item):
        super().__init__()
        self._contentsList = []

        self.contains = contains
        
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            item = self._contentsList[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(item, name.decode())

    def roleNames(self) -> dict[int, QByteArray]:
        d = {}
        for i, field in enumerate(dataclasses.fields(self.contains)):
            d[Qt.ItemDataRole.DisplayRole + i] = field.name.encode()
        return d

    def rowCount(self, parent=None):
        return len(self._contentsList)

    def addItem(self, item: object):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._contentsList.insert(0, item)
        self.endInsertRows()
        
    def moveItem(self, fromIndex: int, toIndex: int):
        self.beginMoveRows(QModelIndex(), fromIndex, fromIndex, QModelIndex(), toIndex)
        self._contentsList.insert(toIndex, self._contentsList.pop(fromIndex))
        self.endMoveRows()
    
    def clear(self):
        self.beginResetModel()
        self._contentsList.clear()
        self.endResetModel()

    def count(self):
        return len(self._contentsList)  
@dataclasses.dataclass
class Tab:
    name: str = ""
    
QML_IMPORT_NAME = "CreateTheSun"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0

@QmlElement
@QmlSingleton
class Backend(QObject):
    modelChanged = QSignal(QAbstractListModel, name="modelChanged", arguments=['model'])
    loadComplete = QSignal(name="loadComplete")
    updateTheme = QSignal(name="updateTheme")
    activeTabChanged = QSignal(name="activeTabChanged")
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Backend, cls).__new__(cls, *args, **kwargs)
            
        print(cls._instance)
        return cls._instance

    @staticmethod
    def create(engine):
        bck = Backend()
        return bck
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._value = 0
            
        self.activeTab = "Main Tab"
        self.model = ListModel()
    
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
    model = ListModel(contains=Tab)
    model.addItem(Tab("Stats"))
    model.addItem(Tab("Save & Load"))
    model.addItem(Tab("Goals"))
    model.addItem(Tab("Achevements"))
    model.addItem(Tab("Automation"))
    model.addItem(Tab("Main Tab"))
    return model

def singleton_provider(engine):
    return Backend()
    
def main():
    theme = materialInterface.Theme()
    theme.get_dynamicColors(0xDCAB5C, True, 0.0)
    app = QApplication()
    
    fonts = urbanistFont.createFonts()
    app.setFont(QFont(fonts[0][0]))
    
    
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    qml = findQmlFile()
    
    if not qml:
        print('Could not find QML file')
        sys.exit(1)
    else:
        engine.load(qml)

    backend = Backend()
    backendId = qmlRegisterSingletonType(Backend, "CreateTheSun", 1, 0, "Backend", singleton_provider)
    
    
    theme = materialInterface.Theme()
    theme.get_dynamicColors(0xDCAB5C, True, 0.0)
    
    engine.rootObjects()[0].setProperty('theme', theme)
    tabModel = createTabModel()
    engine.rootObjects()[0].setProperty('tabsModel', tabModel)
    
    # Main Theme Source Color: #DCAB5C
    backend.loadComplete.emit()
    backend.updateTheme.emit()
    engine.rootObjects()[0].show()
    sys.exit(app.exec())