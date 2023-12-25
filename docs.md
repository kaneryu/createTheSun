# Create the sun

## Installer/Launcher
The launcher is responsible for launching the game, installing the game, and keeping it updated.
### Process
The user will download the installer as a single executable file, and run it to complete the first installation. The instaler will install the launcher in the same directory for the game.
### ToDo
- Show update notes when an update is available
- General cleanup


## Game


## main.py
This python file manages the main window, the stylesheet, and the creation of tabs

### General ToDo
- update stylesheet
    - game looks 6/10
    - redesign in figma?
    
- update how upgrades work
    - all upgrades will be multi level upgrades
    - multi level upgrades can change description, name, cost, purchases, perks etc depending on the level, though it isn't required that they do that

- add some settings
    - ability to change how large numbers are displayed

- implement saving
    - combine gamedefine.py into one dict and save it to a file

- implement Folding
    - rebirths
    - adds a permanant multiplier to quark gain


## tabs.py
This python file manages the creaton and updating of each tab. Current tabs implemented are main tab, and Automation & Upgrades tab.

## maintab.py
This python file is reponsible for defining the main tab.
The main tab contains the way to purchase items at the start of the game, it also shows the amount of the item your currently have.

## electrons.py
This python file is reponsible for defining the electron side bar. The player, by default, will gain 1 electron per second for a maximum of 100 and a minimum of 0.

## game.py
This python file contains functions for game logic, examples include purchaseAchevement, canAffordItem, humanReadableNumber, etc.
The maintabs should do no logic (eg purchases, upgrades etc) on their own, instead calling functions from game.py.

## gamedefine.py
This python file contains all of the definitions for the game, for example, how many quarks the particleAccelerator gives you is defined in gamedefine, as well as howmany quarks you have and what level the particleAccelerator is.

## achevements.py
### Not implemented
This file contains a way to display achevements, though it isn't implemented at all yet.

## upgradetab.py
This python file contains the upgrade tab.



