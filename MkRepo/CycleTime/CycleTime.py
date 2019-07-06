import sys
sys.path.append("..")

import kivy
from Equipment.Equpiment import DummyEquipment


class BaseCycle:
    def __init__(self):
        self.Name = ''
        self.Duration = 0
        self.Equipment = DummyEquipment()

    def getName(self):
        return self.Name

    def getEquipName(self):
        return self.Equipment.Name

    def getDuration(self):


class Mucking(BaseCycle):
    def __init__(self):
        super.__init__()
        self.Name = 'Mucking'


class Drilling(BaseCycle):
    def __init__(self):
        super.__init__()
        pass


class Blasting(BaseCycle):
    def __init__(self):
        super.__init__()
        pass


class Cycles:
    def __init__(self):
        self.Cycles = []


class CycleTime:
    def __init__(self):
        pass



def test():
    pass

if __name__ == "__main__":
    test()
