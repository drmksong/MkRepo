import sys
sys.path.append("..")

import enum
import math

class BlastabilityIndex(enum.Enum):
    GoodBlastability = 0.38
    MediumBlastability = 0.47
    PoorBlastability = 0.56

class CycleInput:
    def __init__(self):
        self.TunnelLength = 0
        self.TunnelCrossSection = 0
        self.RoundLength = 0
        self.DRI = 0
        self.Blastability = BlastabilityIndex.MediumBlastability
        self.SCQuantity = 0
        self.BoltQuantity = 0
        self.ShiftPerDay = 0
        self.HourPerShift = 0
        self.DayPerWeek = 0
        self.HourPerDay = 0
        self.AveOverBreak = 0
        self.BlastOverDrill = 0

        self._CenterHoleArea = 0
        self._NoBurnHoles = 0
        self._NoChargedHoles = 0
        self._NoTotalHoles = 0
        self._DrillFactor = 0
        self._PowderFactorBulk = 0
        self._PowderFactorCartridge = 0
        self._ExplosivePerRound = 0

    def Refresh(self): # if Any of the Input changed, then this function should be called
        self._CenterHoleArea = 66*self.RoundLength-83 #mysterious
        self._NoBurnHoles = round(self._CenterHoleArea/82)
        self._NoChargedHoles = round(10.299*self.TunnelCrossSection^0.5792)-self._NoBurnHoles
        self._NoTotalHoles = round(10.299*self.TunnelCrossSection^0.5792)
        self._DrillFactor = self._NoTotalHoles/self.TunnelCrossSection
        self._PowderFactorBulk = 6.5147*self.TunnelCrossSection^(-0.389)
        self._PowderFactorCartridge = 5.67*self.TunnelCrossSection^(-0.361)
        self._ExplosivePerRound = self.TunnelCrossSection*self.RoundLength*self._PowderFactorCartridge


class BaseCycleTime:
    def __init__(self):
        self.CycleTime = 0


class DrillingCycleTime(BaseCycleTime):
    def __init__(self):
        self.Input = CycleInput()
        self.DrillMoveIn = 0
        self.MoveAlign4Next = 0
        self.DrillBurnCutHole = 0
        self.ChangeBit = 0
        self.LostTime = 0
        self.TotalCycleTime = 0

    def CalcCycleTime(self):
        self.DrillMoveIn = 10+0.1*self.Input.TunnelCrossSection
        self.MoveAlign4Next =


def test():
    pass


if __name__ == "__main__":
    test()
