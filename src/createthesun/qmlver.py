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
    def __init__(self):
        super().__init__()
        self._songs = []

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            song = self._songs[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(song, name.decode())

    def roleNames(self) -> dict[int, QByteArray]:
        d = {}
        for i, field in enumerate(dataclasses.fields(Item)):
            d[Qt.ItemDataRole.DisplayRole + i] = field.name.encode()
        return d

    def rowCount(self, parent=None):
        return len(self._songs)

    def addSong(self, song: Item):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._songs.insert(0, song)
        self.endInsertRows()
        
    def moveSong(self, fromIndex: int, toIndex: int):
        self.beginMoveRows(QModelIndex(), fromIndex, fromIndex, QModelIndex(), toIndex)
        self._songs.insert(toIndex, self._songs.pop(fromIndex))
        self.endMoveRows()
    
    def clear(self):
        self.beginResetModel()
        self._songs.clear()
        self.endResetModel()


class Backend(QObject):
    modelChanged = QSignal(QAbstractListModel, name="modelChanged", arguments=['model'])
    loadComplete = QSignal(name="loadComplete")
    updateTheme = QSignal(name="updateTheme")
    def __init__(self):
        super().__init__()
        
        self.model = ListModel()
        

def findQmlFile() -> str | None:
    # Find the QML file
    for path in [os.path.join(os.path.dirname(__file__), 'qml'), os.path.join(os.path.dirname(__file__))]:
        for file in os.listdir(path):
            if file == 'main~2x3x.qml':
                return os.path.join(path, file)
    return None

    
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
    print(theme.background)
    mod = backend.model
    backend.modelChanged.emit(mod)

    # Main Theme Source Color: #DCAB5C
    backend.loadComplete.emit()
    backend.updateTheme.emit()
    engine.rootObjects()[0].show()
    sys.exit(app.exec())