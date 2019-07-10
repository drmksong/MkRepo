

class BaseEquipment:
    def __init__(self):
        self.Name = ''
        self.Number = 0
        self.Duration = 0

    def setName(self,name):
        self.Name = name

    def setNumber(self,number):
        self.Number = number

    def setDuration(self,duration):
        self.Duration = duration

    def set(self,Name,Number,Duration):
        self.Name = Name
        self.Number = Number
        self.Duration = Duration


class Jumbo(BaseEquipment):
    def __init__(self):
        self.Name = 'Jumbo'
        self.Duration = 0


class ShotMachine(BaseEquipment):
    def __init__(self):
        self.Name = 'ShotMachine'
        self.Duration = 0


class Lifter(BaseEquipment):
    def __init__(self):
        self.Name = 'Lifter'
        self.Duration = 0


class LoadHeader(BaseEquipment):
    def __init__(self):
        self.Name = 'LoadHeader'
        self.Duration = 0


class DummyEquipment(BaseEquipment):
    def __init__(self):
        self.Name = 'Dummy'
        self.Duration = 0

def test():
  jmb = Jumbo()
  jmb.set(Duration = 10, Name = "Jumbo", Number=1 )
  assert jmb.Duration == 10
  print('pass')


if __name__ == "__main__":
    test()
