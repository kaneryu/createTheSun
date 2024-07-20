from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QVBoxLayout, QMessageBox

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
        message.setTextFormat(Qt.TextFormat.MarkdownText)
        self.layout_.addWidget(message)
        self.layout_.addWidget(self.buttonBox)   
        self.setLayout(self.layout_)
        
    def closeEvent(self, event):
        print("\a")
        if self.preventClose:
            event.ignore()
        else:
            self.reject()

class yesNoDialog(CustomDialog):
    def __init__(self, windowTitle, text, preventClose_ = False):
        super().__init__(text, windowTitle, True, preventClose = preventClose_, customQBtn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)

class popupNotificationOld(CustomDialog):
    def __init__(self, windowTitle, text):
        super().__init__(text, windowTitle, cancelable = False, preventClose = False)
    
class okCancelDialog(CustomDialog):
    def __init__(self, windowTitle, text, preventClose_ = False):
        super().__init__(text, windowTitle, True, preventClose = preventClose_)

class badDialog(QMessageBox):
    def __init__(self, text_, windowTitle_, type_):
        super().__init__()
        if type_ == "error":
            self.setIcon(QMessageBox.Icon.Critical)
        elif type_ == "warn":
            self.setIcon(QMessageBox.Icon.Warning)
        elif type_ == "info":
            self.setIcon(QMessageBox.Icon.Information)
            
        self.setWindowTitle(windowTitle_)
        self.setTextFormat(Qt.TextFormat.MarkdownText)
        
        self.setText(text_)


class errorDialog(badDialog):
    def __init__(self, windowTitle, text):
        super().__init__(text_ = text, windowTitle_ = windowTitle, type_ = "error")

class popupNotification(CustomDialog):
    def __init__(self, windowTitle, text):
        super().__init__(text, windowTitle, cancelable = False, preventClose = False)
class warningDialog(badDialog):
    def __init__(self, windowTitle, text):
        super().__init__(text, windowTitle, "warn")
