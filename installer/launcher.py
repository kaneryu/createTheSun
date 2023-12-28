#stdlib imports
import sys
import io
import os
import subprocess
import requests
from win32com.client import Dispatch
from time import sleep
from threading import Thread
import threading
import zipfile
import json
#external imports
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QProgressBar, QDialog, QDialogButtonBox
from PyQt6.QtGui import QPalette, QColor

basedir = os.path.dirname(__file__)
installpath = f"{os.getenv('LOCALAPPDATA')}/createTheSun/"
dark_stylesheet = """
QMainWindow {background: #222222;}
QLabel {color: white;}

QPushButton {
    background: #222222;
    border: 1px solid #ffffff;
    border-radius: 7px;
    color: white;
    padding: 5px;
}
QPushButton:hover {
    background: #ffffff;
    color: #222222;
}
QPushButton:pressed {
    background: #e5e3ff;
    color: #222222;
}
QPushButton:disabled {
    background: #361616;
    color: #ffffff;
}
QProgressBar {
    border: 1px solid #ffffff;
    border-radius: 7px;
    background: #222222;
    color: white;

}

QDialog {
    background: #222222;
    border: 1px solid #ffffff;
    border-radius: 7px;
    color: white;
    padding: 5px;
}

QWidget{
    background: #222222;
}

QTabWidget::pane {
    background: #222222;
    color: white;
}
QTabBar::tab {
    background: #222222;
    color: white;
    border: 1px solid #ffffff;
    border-top-left-radius: 7px; /* For rounded corners */
    border-top-right-radius: 7px;
    min-width: 8ex;
    padding: 2px; /* Padding inside each tab */
    margin-right: 2px;
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
}

QLineEdit {
    background: #222222;
    border: 1px solid #ffffff;
    color: white;
    padding: 2px;
}

QTextEdit {
    color: white;
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
        self.setWindowTitle("Launcher")
        self.setGeometry(100, 100, 500, 100)

        self.progress_signal.connect(self.update_progressbar)
        self.label_signal.connect(self.update_label)
        self.label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter) #type: ignore
        
        self.install_progress_bar = QProgressBar()

        self.container = QWidget()
        self.Vlayout = QVBoxLayout()
        self.startButton = QPushButton("Start Create The Sun")
        self.startButton.clicked.connect(self.startInstall)
        self.Vlayout.addWidget(self.label)
        self.Vlayout.addWidget(self.startButton)
        self.PlaceholderLayout = QVBoxLayout()
        self.Vlayout.addLayout(self.PlaceholderLayout)
        
        self.container.setLayout(self.Vlayout)
        
        self.setCentralWidget(self.container)
        
        
    def startInstall(self):
        self.Vlayout.removeWidget(self.startButton)
        
        if not os.path.exists(installpath):
            dialog = CustomDialog("Would you like to install Create The Sun?", "Install Create The Sun", True)
            results = dialog.exec() 
            
            if results == QDialog.DialogCode.Accepted:
                try:
                    self.install_yes(None)
                except requests.exceptions.ConnectionError:
                    dialog = CustomDialog("There was an error installing Create The Sun. Please check your internet connection and try again.", "Install error", False)
                    dialog.exec()
                    self.close()
                    
                #this will execute after install
                appDatapath = os.getenv("APPDATA")
                if not os.path.exists(f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/"):
                    os.mkdir(f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/")
                    createShortcut( f"{os.getenv('LOCALAPPDATA')}/createTheSun/launcher.exe", f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/Create The Sun.lnk")
                else:
                    removeDir(f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/", False)
                    os.mkdir(f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/")
                    createShortcut( f"{os.getenv('LOCALAPPDATA')}/createTheSun/launcher.exe", f"{appDatapath}/Microsoft/Windows/Start Menu/Programs/Create The Sun/Create The Sun.lnk")
                dialog = CustomDialog("Start Menu entry added", "", False)     
                dialog.exec()              
                self.close()
            else:
                self.close()
        else:
            self.label.setText("Checking for updates...")

            try:
                if self.updateCheck() == 1:
                    self.label.setText("An update is available.")
                    dialog = CustomDialog("Would you like to install the update?", "Update available", True)
                    results = dialog.exec() 
                    if results == QDialog.DialogCode.Accepted:
                        self.install_yes(None)
                    else:
                        self.label.setText("Starting Create The Sun...")
                else:
                    self.label.setText("There are no updates available. Starting Create The Sun...")
            except requests.exceptions.ConnectionError:
                dialog = CustomDialog("Update check failed due to connection error", "Update Failed", False)
                dialog.exec()
        self.start()
                
            
    def updateCheck(self):
        request = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        response = json.loads(request.text)
        self.installpath = f"{os.getenv('LOCALAPPDATA')}/createTheSun/"
        file = open(f"{self.installpath}version.txt", "r")
        currentVersion = file.read()
        file.close()
        self.latestVersion = response[0]["tag_name"]
        
        print(f"Current version: {currentVersion}\nLatest version: {self.latestVersion}")
        
        if request.status_code != 200:
            dialog = CustomDialog("There was an error checking for updates. Would you like to install Create The Sun?", "Update error", True)
            dialog.exec()
        elif currentVersion != self.latestVersion:
            changeLog = self.getChangelog(currentVersion)
            if not changeLog == "No changelog available":
                dialog = CustomDialog(f"There is an update available. Would you like to install it?", "Update available", True, changeLog)
            else:
                dialog = CustomDialog("There is an update available. Would you like to install it?", "Update available", True)
                
            results = dialog.exec() 
            if results == QDialog.DialogCode.Accepted:
                return 1
            else:
                return 0
        else:
            self.label.setText("Create The Sun is up to date.")
            return 0
        
        
    def update_progressbar(self, value):
        self.install_progress_bar.setValue(value)
        return 0
    def update_label(self, text):
        self.label.setText(text)
        return 0

    def install_yes(self, event):
        
        self.PlaceholderLayout.addWidget(self.install_progress_bar)
        self.install_progress_bar.setValue(0)
        self.install_progress_bar.setMaximum(100)
        self.install_progress_bar.setTextVisible(True)
        self.install_progress_bar.setFormat("Downloading... %p%")
        self.install_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.install_progress_bar.setContentsMargins(0, 0, 0, 0)
        
        self.label.setText("Create The Sun is downloading...")
        download = Thread(target=self.download_thread)
        sleep(0.5)
        download.start()
        
        while download.is_alive():
            app.processEvents()
            
        self.install_progress_bar.setFormat("Installing... %p%")
        self.install_progress_bar.setValue(0)
        
        self.label.setText("Create The Sun is installing...")
        
        install = Thread(target=self.install_thread)
        sleep(0.5)
        install.start()
        while install.is_alive():
            app.processEvents()

            
        self.label.setText("Create The Sun is installed.")
        
        self.dialog = CustomDialog("Create The Sun is installed.", "Create The Sun installed.", False)
        self.dialog.exec()
        
    def start(self):
        os.chdir(installpath)
        subprocess.Popen("main.exe")
        self.close()

        
    def download_thread(self):
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        size = 0
        askForUpdate = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        response = json.loads(askForUpdate.text)
        url = response[0]["assets"][0]["browser_download_url"]
        
        with requests.get(url, headers = HEADERS, stream = True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            with open("application.zip", "wb") as f:
                for chunk in r.iter_content(chunk_size = 8192):
                    size = size + f.write(chunk)
                    self.progress_signal.emit(int(size / total_size * 100))
                    if threading.main_thread().is_alive() == False:
                        os.remove("application.zip")
                        return -1
        return 0
    

    def install_thread(self):
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
            self.progress_signal.emit(currentValue / len(self.zipFile.infolist()) * 100)
            self.zipFile.extract(member, installDir)
            if threading.main_thread().is_alive() == False:
                os.remove("application.zip")
                removeDir(installDir)
                return -1
        #os.remove("application.zip")
        self.install_progress_bar.setValue(100)
        return 0

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        sys.exit(0) #stop all threads
        
        
    def getChangelog(self, version):
        request = requests.request("GET", "https://raw.githubusercontent.com/kaneryu/createthesun/master/changelog.json")
        response = json.loads(request.text)
        
        if not version in response:
            return "No changelog available"
        
        rawChangelog = response[version]["text"]
        changelog = ""
        for i in rawChangelog:
            changelog += i + "\n"
        
        request = requests.request("GET", "https://api.github.com/repos/KaneryU/createTheSun/releases")
        response = json.loads(request.text)
        changelog = response[0]["body"]
        return changelog
        
    
class CustomDialog(QDialog):
    def __init__(self, text, windowTitle = "Dialog", cancelable = True, markdownText = ""):
        super().__init__()

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
window = MainWindow()

window.show()

app.exec()