import achevements

class Observable:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for obs in self._observers:
            obs.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        if kwargs["type"] == "purchaseEvent":
            purchaseEvent(observable, *args, **kwargs)
        elif kwargs["type"] == "upgradePurchaseEvent":
            upgradePurchaseEvent(observable, *args, **kwargs)

def purchaseEvent(observable, *args, **kwargs):
    if kwargs["name"] == "quarks":
        while showAchevement("quarks").isVisible():
            pass
        
        return 0

def upgradePurchaseEvent(observable, *args, **kwargs):
    pass

def showAchevement(name):
    popup = achevements.achevementPopup(name, True)
    return popup
g_observable = Observable()
g_receiver = Observer(g_observable)