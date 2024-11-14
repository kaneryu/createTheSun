# stdlib imports
import dataclasses
import random
import os
import random
import sys
import threading
import time


import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, Qt, QTimer, QThread
from PySide6.QtCore import Signal as QSignal
from PySide6.QtCore import Slot as Slot, QDir
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtQml import (
    QmlElement,
    QmlSingleton,
    QQmlApplicationEngine,
    qmlRegisterSingletonInstance,
    qmlRegisterSingletonType,
    QQmlContext
)
from PySide6.QtWidgets import QApplication

# local imports
from .gameLogic import itemGameLogic
from . import materialInterface, urbanistFont, gamedefine, iLoveModelsTotally
from . import ctstime

class BackgroundWorker(QThread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        self.lastElectronIncreaseTime = 0
        while self.running:

            time.sleep(1/60) # 60hz

            if not gamedefine.items["Electrons"].amount >= gamedefine.items["Electrons"].maxAmount and ctstime.getTimeSinceTimestampMs(self.lastElectronIncreaseTime) >= gamedefine.items["Electrons"].waitTime:
                gamedefine.items["Electrons"].amount = gamedefine.items["Electrons"].increaseAmount + gamedefine.items["Electrons"].amount
                self.lastElectronIncreaseTime = ctstime.getTimeMs()

            if gamedefine.items["Electrons"].amount <= gamedefine.items["Electrons"].minAmount:
                gamedefine.items["Electrons"].amount = gamedefine.items["Electrons"].minAmount

            for i in list(gamedefine.items.values()):
                print(i, i.name)
                i.periodicalChecks()


    def stop(self):
        self.running = False
        self.deleteLater()

def startBackgroundWorker():
    worker = BackgroundWorker()
    worker.start()
    return worker


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

    @Property(list, constant=True)
    def tabList(self):
        return [i.internalName for i in tabsModel._contentsList]

    @Slot()
    def applicationExit(self):
        global engine
        engine.destroyed.connect(self.completeApplicationExit)
        engine.deleteLater()


    @Slot()
    def completeApplicationExit(self, stage="nonfinal"):
        bgworker.terminate()
        app.quit()
        sys.exit()


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
    for i in reversed(gamedefine.game.purchaseToCreate):
        ItemsModel.addItem(Item(gamedefine.items[i]))

    gamedefine.game.purchaseToCreateChanged.connect(updateItemModel)

    return ItemsModel

def updateItemModel():
    # first, find deleted items
    global ItemsModel

    for i in range(ItemsModel.count()):
        if ItemsModel._contentsList[i].item.name not in gamedefine.game.purchaseToCreate:
            ItemsModel.removeItem(i)

    # then, find new items
    for i in gamedefine.game.purchaseToCreate:
        found = False
        for j in range(ItemsModel.count()):
            if ItemsModel._contentsList[j].item.name == i:
                found = True
        if not found:
            ItemsModel.addItem(Item(gamedefine.items[i]))

    # move any items that are in the wrong place
    for i in range(ItemsModel.count()):
        if ItemsModel._contentsList[i].item.name != gamedefine.game.purchaseToCreate[i]:
            ItemsModel.moveItem(i, gamedefine.game.purchaseToCreate.index(ItemsModel._contentsList[i].item.name))


def main():
    global app, engine, backend, theme, items, ItemGameLogic, ItemsModel, bgworker, tabsModel
    gamedefine.ItemGameLogic = itemGameLogic.ItemGameLogic
    app = QApplication()

    fonts = urbanistFont.createFonts()
    app.setFont(QFont(fonts[0][0]))


    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    qml = findQmlFile()

    backend = Backend()

    theme = materialInterface.Theme()
    theme.get_dynamicColors(0x18130B, True, 0.0)

    ItemGameLogic = itemGameLogic.ItemGameLogic.getInstance()
    gamedefine.createItems()
    items = Items()
    
    context = engine.rootContext()

    ItemsModel = createItemModel()
    tabsModel = createTabModel()

    context.setContextProperty("Theme", theme)
    context.setContextProperty("Backend", backend)
    context.setContextProperty("ItemGameLogic", ItemGameLogic)
    context.setContextProperty("Items", items)
    context.setContextProperty("TabsModel", tabsModel)
    context.setContextProperty("ItemsModel", ItemsModel)


    if not qml:
        print('Could not find QML file')
        sys.exit(1)
    else:
        engine.load(qml)


    bgworker = startBackgroundWorker()



    # tim = QTimer()
    # tim.setInterval(1000)
    # tim.timeout.connect(lambda: theme.get_dynamicColors(generateRandomHexColor(), True, 0.0))
    # tim.start()

    print(QDir.currentPath())
    bgworker = startBackgroundWorker()
    # Main Theme Source Color: #DCAB5C
    backend.loadComplete.emit()

    app.exec()
