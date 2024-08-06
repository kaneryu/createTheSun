# stdlib imports
import dataclasses
import enum
import os
import random
import sys
import threading
import time

import requests
from PySide6.QtCore import Property as Property

# library imports
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal , Slot



# local imports
from gameLogic import numberLogic



class ItemInteractions(QObject)