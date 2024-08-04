lets see... we need to fix saving (again)

Instead of using nested dictionaries, I want to use classes *and* nested dictionaries. The reason for this is to access the data from the QML using the `@property` decorator. This will allow me to use the `onPropertyChanged` signal to update the QML when the data changes.

When a piece of data needs to be accesed from QML, it will be stored as a class property. When it doesn't, it can be stored in either a class property *or* a dictionary. The dictionary will be used to store data that is not accessed from QML.

Example:
```python
    "quarks": {
        "visualName": "Quarks",
        "description": "Quarks are the building blocks of protons. They are made of nothing...?",
        "id": ["quarks", 0],
    }

    "itemInternalDefine": {
        "quarks": {
            "whatItCosts": [{"what": "nothing", "amount": -1}],
            "defaultCost": -1,
            "costEquation": "",
            "whatItGives": [{"what": "quarks", "amount": 1}],
        }
    }
    # snippet from gamedefine
```
In this example, `quarks` will become a class. `visualName`, `description`, and `id` will be class properties. `whatItCosts`, `defaultCost`, `costEquation`, and `whatItGives` will be stored in the nested dictionary. as a class variable.

Actual Saving:
Instead of saving the JSON, I will save it in a SQLite database.

Currently: All changes to item (for example costs) are made *directly* to the gamedefine dictionary. Then, during saving, we step through each key in gamedefine to see if it was changed. If so, we then save that key. This works, but I think it's inefficient.

All changes are not random. for example, the cost of protons is only changed when the user purcases the rewrite "quark efficiency". So, I will use "switch" items to store each change indiviually. The used switch item will change depending on what the user does. The only thing that needs to be stored is a number indicating which switch to use. This will be stored in the database.
The amount of each item a player has will be stored in the db also.