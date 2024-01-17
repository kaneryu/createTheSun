#stdlib imports
import sys
import io
import os
import subprocess
import requests
import time
from win32com.client import Dispatch
from time import sleep
from threading import Thread
import threading
import zipfile
import json
import shutil
#external imports
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


basedir = os.path.dirname(__file__)
installpath = f"{os.getenv('LOCALAPPDATA')}/createTheSun/"
dark_stylesheet = """
QWidget{
    background: #1e1e1e;
    color: white;
    font-family: "Urbanist Medium";
    font-size: 15px;
}
QMainWindow{
    background: #1e1e1e;
    border-radius: 10px;
}
QLabel {
    color: white;
    background: transparent;
    font-family: "Urbanist Medium";
    font-size: 15px;
    
}
QLineEdit {
    font-family: "Urbanist Medium";
}
/*222222*/
QPushButton {
    background: #1e1e1e;
    border: 1px solid #ffffff;
    border-radius: 7px;
    color: white;
    padding: 5px;
    font-family: "Urbanist Medium";
    font-size: 15px;
}
QPushButton:hover {
    background: #ffffff;
    color: #1e1e1e;
}
QPushButton:pressed {
    background: #e5e3ff;
    color: #1e1e1e;
    font-family: "Urbanist Black";
}
QPushButton:disabled {
    background: #361616;
    color: #ffffff;
}
QProgressBar {
    border: 1px solid #ffffff;
    background: #494949;
    color: #2600ff;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #ffffff;
}

QDialog {
    background: #1e1e1e;
    border: 1px solid #ffffff;
    border-radius: 7px;
    color: white;
    padding: 5px;
}

QWidget{
    background: #1e1e1e;
}

QTabWidget::pane {
    background: #1e1e1e;
    color: white;
}
QTabBar::tab {
    background: #1e1e1e;
    color: white;
    border: 1px solid #ffffff;
    border-top-left-radius: 7px; /* For rounded corners */
    border-top-right-radius: 7px;
    min-width: 8ex;
    padding: 2px; /* Padding inside each tab */
    margin-right: 2px;
    font-family: "Urbanist Light";
}
QTabBar::tab:selected {
    background: #2e2e2e;
    color: white;
    border: 2px solid #ffffff;
    border-top-left-radius: 7px; /* For rounded corners */
    border-top-right-radius: 7px;
    min-width: 8ex;
    padding: 2px; /* Padding inside each tab */
    margin-right: 2px;
    font-family: "Urbanist Medium";
}

QLineEdit {
    background: #1e1e1e;
    border: 1px solid #ffffff;
    color: white;
    padding: 2px;
}

QErrorMessage::QTextEdit{
    color: #ffffff;
}

QComboBox
{
    color:white;
    border-color: rgba(255,255,255,200);
    border-width: 1px;
    border-style: solid;
    padding: 1px 0px 1px 3px; /*This makes text colour work*/
}
QWidget:item
{
    color: white;
    border: 0px solid #999900;
    background: transparent;
}
QWidget:item:checked
{
     font-weight: bold;
}
"""

def createShortcut(path, target):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(target)
    shortcut.Targetpath = path
    shortcut.save()

def removeDir(dir, warning = True) -> None:
    if warning == True:
        print("WARNING!!! THIS WILL DELETE ALL FILES IN THE DIRECTORY AND THE DIRECTORY ITSELF!!!")
        sleep(30)
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            print(f"Removing {os.path.join(root, name)}")
            os.remove(os.path.join(root, name))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            print(f"Removing {os.path.join(root, name)}")
            os.rmdir(os.path.join(root, name))
    os.rmdir(dir)

class MainWindow(QMainWindow):
    progress_signal = pyqtSignal(int)
    label_signal = pyqtSignal(str)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Installer")
        
        screen: QScreen = app.primaryScreen() #type: ignore
        screen_size = screen.geometry()
        screenCenter = screen_size.center()
        
        self.setGeometry(screenCenter.x() - 500//2 ,screenCenter.y() - 200//2,500,200)
        
        container = QWidget()
        
        self.installerProgressBar = QProgressBar()
        self.installerProgressBar.setRange(0, 0)
        
        self.installerLabel = QLabel("Contacting GitHub...")
        self.installerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installerLabel.setWordWrap(True)
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.installerLabel)
        layout.addWidget(self.installerProgressBar)
        
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        timer = QTimer(self)
        timer.timeout.connect(self.checkConnection)
        timer.setSingleShot(True)
        timer.start(1000)
        
        
    def getChangelog(self, version):
        request = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        response = json.loads(request.text)
        changelog = response[0]["body"]
        return changelog
    
    def checkConnection(self):
        if requests.get("https://api.github.com").status_code == 200:
            self.installerLabel.setText("")
            askForPermission = changeLogDialog(f"Do you want to install the game?", "Create The Sun", True, self.getChangelog("v1.0.0"))
            askForPermission.exec()
            if askForPermission.result() == 1:
                self.downloadLatestRelease()
            else:
                self.close()
        else:
            self.installerLabel.setText("No internet connection")
            self.installerProgressBar.setRange(0, 0)
            

    def downloadLatestRelease(self):
        self.installerLabel.setText("Downloading latest release...")
        self.progress_signal.connect(self.installerProgressBar.setValue)
        self.label_signal.connect(self.installerLabel.setText)
    
        self.installerProgressBar.setRange(0, 100)
        self.installerProgressBar.setValue(0)
        
        thread = Thread(target=self.downloadThread)
        thread.start()
        
        while thread.is_alive():
            app.processEvents()
        
        self.label_signal.emit("Extracting files...")

        thread = Thread(target=self.extractThread)
        thread.start()
        
        while thread.is_alive():
            app.processEvents()
        
        self.label_signal.emit("Creating shortcut...")
        createShortcut(installpath + "main.exe", os.path.join(os.getenv("APPDATA"), "Microsoft/Windows/Start Menu/Programs/Create The Sun.lnk")) #type: ignore
        
        complete = CustomDialog("Installation complete.", "Create The Sun Installer", False)
        complete.exec()
        app.quit()
        
    def downloadThread(self):
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        size = 0
        askForLatest = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        response = json.loads(askForLatest.text)
        url = response[0]["assets"][0]["browser_download_url"]

        with requests.get(url, headers = HEADERS, stream = True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            with open("application.zip", "wb") as f:
                
                for chunk in r.iter_content(chunk_size = 8192):
                    size = size + f.write(chunk)
                    self.progress_signal.emit(int(size / total_size * 100))
                    self.label_signal.emit(f"Downloading: {size / 1000000:.2f} MB / {total_size / 1000000:.2f} MB")
                    if threading.main_thread().is_alive() == False:
                        f.close()
                        os.remove("application.zip")
                        return -1
        return 0

    def extractThread(self):
        self.zipFile = zipfile.ZipFile("application.zip")
        installDir = os.getenv("LOCALAPPDATA") + "/createTheSun/" #type: ignore
        if not os.path.exists(installDir):
            os.mkdir(installDir)
        else:
            self.label_signal.emit("Removing old files...")
            removeDir(installDir, False)
            self.label_signal.emit("Installing...")
            os.mkdir(installDir)
        
        currentValue = 0
        for member in self.zipFile.infolist():
            currentValue += 1
            self.progress_signal.emit(int(currentValue / len(self.zipFile.infolist()) * 100))
            
            self.label_signal.emit(f"Extracting Files: {member.filename}")
            self.zipFile.extract(member, installDir)
            
            if threading.main_thread().is_alive() == False:
                self.zipFile.close()
                os.remove("application.zip")
                removeDir(installDir)
                return -1

        self.zipFile.close()
        os.remove("application.zip")
        self.progress_signal.emit(100)
        
        request = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        version = json.loads(request.text)[0]["tag_name"]
        with open(installDir + "version.txt", "w") as f:
            f.write(version)
        
        if os.path.exists(os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/"): #type: ignore
            removeDir(os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/", False) #type: ignore
            os.mkdir(os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/") #type: ignore
        else:
            os.mkdir(os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/") #type: ignore
            
        with open(os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/icon.ico", "wb") as f: #type: ignore
            f.write(requests.request("GET", "https://raw.githubusercontent.com/KaneryU/createTheSun/main/assets/images/icon.ico").content) #type: ignore
            
        shutil.copy(__file__, os.getenv("LOCALAPPDATA") + "/createTheSunUpdater/") #type: ignore
        
        return 0
    
class CustomDialog(QDialog):
    def __init__(self, text, windowTitle = "Dialog", cancelable = True, customQBtn = None, preventClose = False):
        super().__init__()

        self.setWindowTitle(windowTitle)
        if customQBtn == None:
            if cancelable == True:
                QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            else:
                QBtn = QDialogButtonBox.StandardButton.Ok
        else:
            QBtn = customQBtn
            
        self.preventClose = preventClose
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout_ = QVBoxLayout()
        message = QLabel(text)
        self.layout_.addWidget(message)
        self.layout_.addWidget(self.buttonBox)   
        self.setLayout(self.layout_)
        
    def closeEvent(self, event):
        print("\a")
        if self.preventClose:
            event.ignore()
        else:
            self.reject()

class changeLogDialog(QDialog):
    def __init__(self, text, windowTitle = "Dialog", cancelable = True, markdownText = ""):
        super().__init__()
        self.setGeometry(100, 100, 600, 500)
        self.setWindowTitle(windowTitle)
        if cancelable == True:
            QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        else:
            QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_ = QVBoxLayout()
        message = QTextEdit(text)
        if markdownText != "":
            message.setMarkdown(markdownText)
        message.setReadOnly(True)
        self.layout_.addWidget(message)
        self.layout_.addWidget(self.buttonBox)
        self.setLayout(self.layout_)
        
        
app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "icon.ico")))
app.setStyleSheet(dark_stylesheet)

splash = QSplashScreen(QtGui.QPixmap(os.path.join(basedir, "icon.ico")))
splash.show()
for i in range(1):
    splash.showMessage("Preparing for the installation" + "." * i, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, color=QtGui.QColor("white"))
    time.sleep(1)

window = MainWindow()

window.show()
splash.hide()
app.exec()