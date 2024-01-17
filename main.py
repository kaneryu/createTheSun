#standard imports
import time
import ctypes
import threading
import sys
import os
import json
import requests
import subprocess
#third party imports
# from PyQt6 import QtCore
# from PyQt6.QtGui import QIcon
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QSizePolicy, QMessageBox, QDialog
# from PyQt6.QtCore import QPropertyAnimation, Qt, QTimer, QRunnable, pyqtSlot, pyqtSignal, QThreadPool
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QSizePolicy, QMessageBox, QDialog
from PySide6.QtCore import QPropertyAnimation, Qt, QTimer, QRunnable, Slot as pyqtSlot, Signal as pyqtSignal, QThreadPool

#local imports
import observerModel
import gamedefine
import tabs_ as tabs
import tabs.electrons as electrons
import logging_ as logging
import assets.fonts.urbanist.urbanistFont as urbanistFont

logging.logLevel = 1
logging.specialLogs = []
basedir = os.path.dirname(__file__)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class MainWindow(QMainWindow):
    updateSignal = pyqtSignal()
    sUpdateThread1 = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.threadpool = QThreadPool()
        self.updateSignal.connect(self.updateDisplay)
        self.sUpdateThread1.connect(self.sUpdateThread1)
        logging.log("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount(), 1)

        
        self.setWindowTitle("Create The Sun")
        self.tabWidget = QTabWidget()
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.tabs = []

        for i in tabs.tabs:
            self.tabs.append({"class" : i(), "name": i.name()})
            self.tabWidget.addTab(self.tabs[-1]["class"], i.name())
            self.tabWidget.setTabToolTip(len(self.tabs) - 1, i.tooltip())

        self.tabWidget.setMovable(True)
        self.topContainer = QWidget()
        self.label = QLabel("Create The Sun")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topContainerLayout = QHBoxLayout()
        self.topContainerLayout.addWidget(self.label)
        self.topContainer.setLayout(self.topContainerLayout)
        
        self.layout: QVBoxLayout = QVBoxLayout()
        self.contentLayout = QHBoxLayout()
        self.contentContainer = QWidget()
        
        self.layout.addWidget(self.topContainer)
        self.contentLayout.addWidget(self.tabWidget)
        
        self.electrons = electrons.electrons()
        self.contentLayout.addWidget(self.electrons)
        
        self.contentContainer.setLayout(self.contentLayout)
        self.layout.addWidget(self.contentContainer)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        
        self.setCentralWidget(self.container)

        
        self.displayUpdate = Worker(self._updateDisplay)
        self.interalUpdate1 = Worker(self.updateThread1)
        self.threadpool.start(self.displayUpdate)
        self.threadpool.start(self.interalUpdate1)


    def _updateDisplay(self):
        """
        Updates the display continuously.
        Because this function directly interacts with the Qt Gui, there must be a short pause between updates,
        or else there will be general instability in the application.        
        """
        while True:
            self.updateSignal.emit()
            time.sleep(0.001)
            if not threading.main_thread().is_alive():
                return

            
            
    def updateDisplay(self):
        """
        Updates the display by calling the updateDisplay method whatever needs to be updated.
        """
        for i in self.tabs:
            logging.log(f"now updating tab {i["name"]}", specialType="updateLoopInfo")
            i["class"].updateDisplay()

        logging.log("now updating electrons", specialType="updateLoopInfo")
        self.electrons.updateDisplay()
        if not threading.main_thread().is_alive():
            return
    
    def updateThread1(self):
        """
        A seperate thread for updating electrons and tabs, so it can run as fast as possible without waiting for display referesh
        """
        while True:
            self.electrons.updateInternal()
            self.tabs[1]["class"].updateInternal()
            self.tabs[2]["class"].updateInternal()
            
            if not threading.main_thread().is_alive():
                return 0
            
            if gamedefine.force == 1:
                gamedefine.force = 0
                forceUpdate()
            
    def forceUpdate(self):
        """
        Forces an update of the display by calling the updateEverything method of some tabs.
        """
        #update automation tab
        self.tabs[1]["class"].updateEverything()

        self.electrons.updateDisplay()
    
    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        self.displayUpdate.autoDelete()
        self.interalUpdate1.autoDelete()
        
        saveDialog = tabs.saveModule.CustomDialog("Would you like to save your game?", "Save game", True)
        saveDialogResults = saveDialog.exec()
        if saveDialogResults == QDialog.DialogCode.Accepted:
            tabs.saveModule.save(notify = False)
        
        sys.exit(0) #stop all threads
        
    # def createSaveDir(self):
    #     LOCALAPPDATA = os.getenv('LOCALAPPDATA')
    #     if not LOCALAPPDATA:
    #         LOCALAPPDATA = os.path.join(os.getenv('APPDATA'), r"\Local") #type:ignore
            
    #     SAVEDIR = os.path.join(LOCALAPPDATA, r"CreateTheSun\Saves")
        
    #     if not os.path.exists(SAVEDIR):
    #         os.mkdir(SAVEDIR)

def preStartUp():
    def updateCheck():
        try:
            request = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        except:
            return True
        
        response = json.loads(request.text)
        installpath = os.path.dirname(__file__) + "\\"
        
        try:
            file = open(f"{installpath}version.txt", "r")
        except FileNotFoundError:
            file = open(f"{installpath}version.txt", "w")
            file.write("-1.0.0")
            file.close()
            file = open(f"{installpath}version.txt", "r")

        currentVersion = file.read()
        file.close()
        latestVersion = response[0]["tag_name"]
        print(f"current version: {currentVersion}, latest version: {latestVersion}")
        if currentVersion == latestVersion:
            return True
        else:
            return False
            
    if not updateCheck(): # if not on the latest version
        if os.path.exists(os.path.dirname(__file__) + "\\_internal"):
            command = f"{os.getenv('LOCALAPPDATA')}\\'/createTheSunUpdater\\installer.exe"
        else:
            return
        
        if not os.path.exists(command):
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(r'You are not on the latest version and the launcher is missing. Please download the latest version from https:\\github.com\KaneryU\createTheSun')
        
        print(command)
        subprocess.Popen([command])
        app.exit()

if __name__ == "__main__":


    
    #change icon in taskbar
    myappid = u'opensource.createthesun.main.pre-release'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    file = open(os.path.join(basedir, 'assets', 'stylesheet.qss'), 'r')
    stylesheet = file.read()
    file.close()
    
    app = QApplication([])

    preStartUp() 
    
    app.setWindowIcon(QIcon(basedir + r"\assets\images\icon.ico"))

    window = MainWindow()
        
    def forceUpdate():
        window.forceUpdate()
        
    urbanistFont.createFonts()
    app.setStyleSheet(stylesheet)
    
    
    
    if  window.threadpool.maxThreadCount() < 2:
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText('You have less than 2 available threads. At least 2 threads are needed to run the game')
        error_dialog.exec()
        sys.exit() 
    
            
    if tabs.saveModule.lookForSave():
        dialog = tabs.saveModule.CustomDialog("It appears you have a save. Would you like to load it?", "Load save", True)
        dialogResults = dialog.exec()
        if dialogResults == QDialog.DialogCode.Accepted:
            tabs.saveModule.load(noSpeak = True)
    
    window.show()
    app.exec()
