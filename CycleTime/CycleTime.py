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
# General Estimate Properties and Assumptions
        self.TunnelLength = 1158 # should be revised, just for testing
        self.TunnelCrossSection = 72.5 # in square meter
        self.RoundLength = 4
        self.DRI = 40
        self.Blastability = BlastabilityIndex.MediumBlastability
        self.SCQuantity = 1.14
        self.BoltQuantity = 3.96
        self.UseCatridge = True

#Labor/Working Time Assumption
        self.ShiftPerDay = 2
        self.HourPerShift = 12
        self.DayPerWeek = 6.5
        self.ProductionHourPerDay = 24

#Drill+Blast Excavation
        self.AveOverBreak = 5 # in percent
        self.BlastOverDrill = 10 # in percent

        self._CenterHoleArea = 66*self.RoundLength-83 # in square cm
        self._NoBurnHoles = round(self._CenterHoleArea/82+0.5) # each hole has 83 cm2
        self._NoChargedHoles = round(10.299*math.pow(self.TunnelCrossSection,0.5792)+0.5) - self._NoBurnHoles
        self._NoTotalHoles = self._NoBurnHoles + self._NoChargedHoles
        self._DrillFactor = self._NoTotalHoles/self.TunnelCrossSection
        self._PowderFactorBulk = 6.5147*math.pow(self.TunnelCrossSection,-0.389)
        self._PowderFactorCartridge = 5.67*math.pow(self.TunnelCrossSection,-0.361)
        if self.UseCatridge:
            self._ExplosivePerRound = self.TunnelCrossSection * self.RoundLength * self._PowderFactorCartridge
        else:
            self._ExplosivePerRound = self.TunnelCrossSection * self.RoundLength * self._PowderFactorBulk

#Mucking Production Loader

        self.SwellFactor = 1.6
        self.LoaderFillFactor = 0.85
        self.PayloadCapacity = 5  # m3
        self.LoadnDumpTime = 0.75  # min
        self.WaitTime = 0.25  # min
        self.NumberLoader = 1
        self._AvailablePayloadCapacity = self.LoaderFillFactor*self.PayloadCapacity/self.SwellFactor
        self._LoaderCycleTime = self.LoadnDumpTime + self.WaitTime  # min
        self.LoaderProductionRate = self._AvailablePayloadCapacity*(60/self._LoaderCycleTime)*self.NumberLoader


    def Refresh(self): # if Any of the Input changed, then this function should be called
        self._CenterHoleArea = 66*self.RoundLength-83 #mysterious
        self._NoBurnHoles = round(self._CenterHoleArea/82+0.5)
        self._NoChargedHoles = round(10.299*math.pow(self.TunnelCrossSection,0.5792)+0.5) - self._NoBurnHoles
        self._NoTotalHoles = self._NoBurnHoles + self._NoChargedHoles
        self._DrillFactor = self._NoTotalHoles/self.TunnelCrossSection
        self._PowderFactorBulk = 6.5147*math.pow(self.TunnelCrossSection,-0.389)
        self._PowderFactorCartridge = 5.67*math.pow(self.TunnelCrossSection,-0.361)
        if self.UseCatridge:
            self._ExplosivePerRound = self.TunnelCrossSection*self.RoundLength*self._PowderFactorCartridge
        else:
            self._ExplosivePerRound = self.TunnelCrossSection * self.RoundLength * self._PowderFactorBulk

        self._AvailablePayloadCapacity = self.LoaderFillFactor*self.PayloadCapacity/self.SwellFactor
        self._LoaderCycleTime = self.LoadnDumpTime + self.WaitTime  # min
        self.LoaderProductionRate = self._AvailablePayloadCapacity*(60/self._LoaderCycleTime)*self.NumberLoader


class BaseCycleTime:
    def __init__(self):
        self.Input = CycleInput()

class DrillingCycleTime(BaseCycleTime):
    def __init__(self):
        self.NoBoom = 3
        self.DrillMoveInTime = = 10+0.1*self.Input.TunnelCrossSection
        self.MoveAlign4Next = self.Input._NoTotalHoles*self.NoBoom*(0.55+0.04*(1+self.Input.BlastOverDrill))  # min
        self.DrillBurnCutHole = 0
        self.ChangeBit = 0
        self.LostTime = 0
        self.TotalCycleTime = 0


    def CalcCycleTime(self):
        self.DrillMoveInTime = 10+0.1*self.Input.TunnelCrossSection
        self.MoveAlign4Next = self.Input._NoTotalHoles*(0.55+0.04*(1+self.Input.BlastOverDrill))/self.NoBoom  # min
        self.DrillBurnCutHole = self.Input._NoBurnHoles



def test():
    cycinput = CycleInput()
    cycinput.UseCatridge = False
    cycinput.Refresh()
    print (cycinput._ExplosivePerRound)
    assert round(cycinput._ExplosivePerRound) == 357
    assert round(cycinput.LoaderProductionRate) == 159
    print('pass')

if __name__ == "__main__":
    test()
