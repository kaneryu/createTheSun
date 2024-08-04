class A:
    def __init__(self):
        print("A")

class B:
    def __init__(self):
        print("B")

class C(A, B):
    def initAll(cls):
        _ = list(cls.__mro__); _.remove(object); _.remove(cls)
        for i in _:
            i.__init__()
            
    def __init__(self):
        self.initAll()



C()