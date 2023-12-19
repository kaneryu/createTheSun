#standard imports
import time
import ctypes
import threading
import sys
from math import floor, ceil, log
#third party imports
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
#local imports
import tabs
import electrons
import _logging as logging

logging.logLevel = 1
logging.specialLogs = []

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
        self.setWindowIcon(QIcon("icon.ico"))
        self.tabWidget = QTabWidget()
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.tabs = []
        
        for i in tabs.tabs:
            self.tabs.append({"class" : i(), "name": i.__name__})
            self.tabWidget.addTab(self.tabs[-1]["class"], self.tabs[-1]["name"])
        
        self.topContainer = QWidget()
        self.label = QLabel("Create The Sun")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topContainerLayout = QHBoxLayout()
        self.topContainerLayout.addWidget(self.label)
        self.topContainer.setLayout(self.topContainerLayout)
        
        self.layout = QVBoxLayout()
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

        displayUpdate = Worker(self._updateDisplay)
        interalUpdate1 = Worker(self.updateThread1)
        self.threadpool.start(displayUpdate)
        self.threadpool.start(interalUpdate1)
        
    
    def _updateDisplay(self):
        """
        Updates the display continuously until the main thread is no longer alive.

        This method emits the updateSignal and then sleeps for a short duration.
        It checks if the main thread is still alive, and if not, it returns 0.

        Returns:
            int: 0 if the main thread is no longer alive.
        """
        while True:
            self.updateSignal.emit()
            time.sleep(0.001)
            if not threading.main_thread().is_alive():
                return 0
            
    def updateDisplay(self):
        """
        Updates the display by calling the updateDisplay method of each tab and the electrons.
        """
        for i in self.tabs:
            logging.log(f"now updating tab {i["name"]}", specialType="updateLoopInfo")
            i["class"].updateDisplay()

        logging.log("now updating electrons", specialType="updateLoopInfo")
        self.electrons.updateDisplay()
    
    def updateThread1(self):
        """
        Updates the internal state of electrons and the class of tab 1.
        
        This method is intended to be run in a separate thread. It continuously updates the internal state of electrons and the class of tab 1. It also checks if the main thread is still alive and returns 0 if it's not.
        """
        while True:
            self.electrons.updateInternal()
            self.tabs[1]["class"].updateInternal()
            
            if not threading.main_thread().is_alive():
                return 0
            
            
        
        

if __name__ == "__main__":
    #change icon in taskbar
    myappid = u'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    file = open('stylesheet.qss', 'r')
    stylesheet = file.read()
    file.close()

    app = QApplication([])
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    if  window.threadpool.maxThreadCount() < 2:
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText('You have less than 2 available threads. At least 2 threads are needed to run the game')
        error_dialog.exec()
        sys.exit() 
    window.show()
    app.exec()