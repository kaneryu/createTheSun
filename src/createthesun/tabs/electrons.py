import time

from PySide6 import QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from .. import gamedefine


class electrons(QWidget):
    def updateDisplay(self):
        self.amountBar.setValue(gamedefine.gamedefine.amounts["electrons"])
        self.label.setText(f"{gamedefine.gamedefine.amounts["electrons"]}")

    def updateInternal(self):
        if time.time() * 1000 - self.lastTickTime > gamedefine.gamedefine.electronDetails["waitTime"]:
            self.lastTickTime = time.time() * 1000
            gamedefine.gamedefine.amounts["electrons"] += gamedefine.gamedefine.electronDetails["amount"]

            if gamedefine.gamedefine.amounts["electrons"] > gamedefine.gamedefine.electronDetails["maxAmount"]:
                gamedefine.gamedefine.amounts["electrons"] = gamedefine.gamedefine.electronDetails["maxAmount"]

            if gamedefine.gamedefine.amounts["electrons"] < gamedefine.gamedefine.electronDetails["minAmount"]:
                gamedefine.gamedefine.amounts["electrons"] = gamedefine.gamedefine.electronDetails["minAmount"]

    def __init__(self):
        super().__init__()
        self.lastTickTime = 0
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_.addWidget(self.label)

        self.amountBar = QProgressBar()
        self.amountBar.setMaximum(100)
        self.amountBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.amountBar.setFormat("")
        self.setToolTip("Electrons")

        self.layout_.addWidget(self.amountBar)

        self.setLayout(self.layout_)
