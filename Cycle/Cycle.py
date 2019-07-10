import sys
sys.path.append("..")
from Equipment.Equpiment import DummyEquipment

class BaseCycle:
    def __init__(self):
        self.Name = ''
        self.Duration = 0
        self.Equipment = DummyEquipment()

    def setName(self,name):
        self.Name = name

    def setDuration(self,dur):
        self.Duration = dur

    def setEquipment(self,equip):
        self.Equipment = equip

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


def test():
    pass


if __name__=='__main__':
    test()