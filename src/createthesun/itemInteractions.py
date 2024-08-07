# stdlib imports
import dataclasses
import enum
import os
import random
import sys
import threading
import typing

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal , Slot



# local imports
from .gameLogic import itemGameLogic
from . import gamedefine


class ItemInteractions(QObject):
    def __init__(self):
        super().__init__()
        self.possibleItems = gamedefine.items.keys()
        
        for i in itemGameLogic.functions:
            self.__setattr__(i.__name__, i)
        
        