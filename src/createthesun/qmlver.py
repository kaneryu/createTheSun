# stdlib imports
import sys
import random
import dataclasses
import requests
import threading
import enum
import os
# library imports
from PySide6.QtCore import Qt, Signal as QSignal, Slot as Slot, QObject, QAbstractListModel, QModelIndex, QTimer, Property as Property, QByteArray
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# local imports
from . import materialInterface
from . import urbanistFont

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
    contents: str = ""


class Backend(QObject):
    modelChanged = QSignal(QAbstractListModel, name="modelChanged", arguments=['model'])
    loadComplete = QSignal(name="loadComplete")
    updateTheme = QSignal(name="updateTheme")
    
    activeTabChanged = QSignal(name="activeTabChanged")
    def __init__(self):
        super().__init__()
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
    model.addItem(Tab("Stats", "Contents 4"))
    model.addItem(Tab("Save & Load", "Contents 4"))
    model.addItem(Tab("Goals", "Contents 4"))
    model.addItem(Tab("Achevements", "Contents 3"))
    model.addItem(Tab("Automation", "Contents 2"))
    model.addItem(Tab("Main Tab", "Contents 1"))
    return model

    
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
    engine.rootObjects()[0].setProperty('backend', backend)
    
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