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
    def __init__(self,cycinput : CycleInput):
        self.Input = cycinput
        self.TotalCycTime = 0

    def Refresh(self):
        self.Input.Refresh()
        self.TotalCycTime = 0


class DrillingCycleTime(BaseCycleTime):
    def __init__(self, cycinput : CycleInput):
        super().__init__(cycinput)
        self.NoBoom = 3
        self._DrillLength = self.Input.RoundLength*(1+self.Input.BlastOverDrill/100.0)
        self.DrillMoveInTime = 10+0.1*self.Input.TunnelCrossSection
        self.MoveAlign4Next = self.Input._NoTotalHoles*(0.55+0.04*(self._DrillLength)) / self.NoBoom  # min
        self.DrillBurnCutHole = self.Input._NoBurnHoles*self._DrillLength*(0.0143*self.Input.DRI+0.8143)*48/102*1.25/self.NoBoom
        self.DrillBlastHole = self.Input._NoChargedHoles*self._DrillLength / 1.39 /self.NoBoom # TODO : replace 1.39 with function, drilling speed
        self.ChangeBit = 1.5 * (self.Input._NoTotalHoles*self._DrillLength) * 0.02 /self.NoBoom #TODO : replace 0.02 with function, change frequency per drill meter
        self.LostTime = ((1.4*math.pow(self.Input.TunnelCrossSection, -0.84)+0.92*math.pow(self.Input.TunnelCrossSection,-0.61))/2.0)*(self.MoveAlign4Next+self.DrillBurnCutHole+self.DrillBlastHole)
        self.TotalCycleTime = self.DrillMoveInTime+self.MoveAlign4Next+self.DrillBurnCutHole+self.DrillBlastHole+self.ChangeBit+self.LostTime

    def Refresh(self):
        super().Refresh()
        self.Input.Refresh()
        self._DrillLength = self.Input.RoundLength*(1+self.Input.BlastOverDrill/100.0)
        self.DrillMoveInTime = 10+0.1*self.Input.TunnelCrossSection
        self.MoveAlign4Next = self.Input._NoTotalHoles*(0.55+0.04*(1+self.Input.BlastOverDrill/100)) / self.NoBoom # min
        self.DrillBurnCutHole = self.Input._NoBurnHoles*self._DrillLength*(0.0143*self.Input.DRI+0.8143)*48/102*1.25/self.NoBoom
        self.DrillBlastHole = self.Input._NoChargedHoles*self._DrillLength* 1.39 /self.NoBoom # TODO : replace 1.39 with function, drilling speed
        self.ChangeBit = 1.5 * (self.Input._NoTotalHoles*self._DrillLength) * 0.02 /self.NoBoom
        drilltotlen = self._DrillLength*self.Input._NoTotalHoles
        self.LostTime = (1.4*(math.pow(drilltotlen, -0.84)+0.92*math.pow(drilltotlen,-0.61))/2.0)*(self.MoveAlign4Next+self.DrillBurnCutHole+self.DrillBlastHole)
        self.TotalCycleTime = self.DrillMoveInTime+self.MoveAlign4Next+self.DrillBurnCutHole+self.DrillBlastHole+self.ChangeBit+self.LostTime


class BlastingCycleTime(BaseCycleTime):
    def __init__(self, cycinput : CycleInput):
        super().__init__(cycinput)
        self.NoCharger = 1
        self._DrillLength = self.Input.RoundLength * (1 + self.Input.BlastOverDrill / 100.0)
        self.ChargeHoleFixedTime = self.Input._NoTotalHoles*0.35/self.NoCharger
        self.ChargeHoleLenDepTime = self.Input._NoTotalHoles*self._DrillLength *0.3/self.NoCharger
        self.StemmingTime = self.Input._NoTotalHoles*0.215/self.NoCharger
        self.WireUpTime = self.Input._NoTotalHoles*0.15/self.NoCharger+10
        self.EvacuateTime = 5
        self.TotalCycleTime = self.ChargeHoleFixedTime + self.ChargeHoleLenDepTime + self.StemmingTime + self.WireUpTime + self.EvacuateTime

    def Refresh(self):
        super().Refresh()
        self._DrillLength = self.Input.RoundLength * (1 + self.Input.BlastOverDrill / 100.0)
        self.ChargeHoleFixedTime = self.Input._NoTotalHoles*0.35/self.NoCharger
        self.ChargeHoleLenDepTime = self.Input._NoTotalHoles*self._DrillLength *0.3/self.NoCharger
        self.StemmingTime = self.Input._NoTotalHoles*0.215/self.NoCharger
        self.WireUpTime = self.Input._NoTotalHoles*0.15/self.NoCharger+10
        self.EvacuateTime = 5
        self.TotalCycleTime = self.ChargeHoleFixedTime + self.ChargeHoleLenDepTime + self.StemmingTime + self.WireUpTime + self.EvacuateTime


class VentCycleTime(BaseCycleTime):
    def __init__(self, cycinput : CycleInput):
        super().__init__(cycinput)
        self.VentTime = 0.3338 * self.Input._NoTotalHoles
        self.TotalCycTime = self.VentTime

    def Refresh(self):
        super().Refresh()
        self.VentTime = 0.3338 * self.Input._NoTotalHoles
        self.TotalCycTime = self.VentTime


class ScalingCyCleTime(BaseCycleTime):
    def __init__(self, cycinput : CycleInput):
        super().__init__(cycinput)
        self._DrillLength = self.Input.RoundLength * (1 + self.Input.BlastOverDrill / 100.0)
        if self.Input.Blastability=="Good":
            self.ScaleTime = 6 + 0.4 * self.Input.TunnelCrossSection
        elif self.Input.Blastability=="Poor":
            self.ScaleTime = 35 + 0.65 * self.Input.TunnelCrossSection
        else:
            self.ScaleTime = ((6 + 0.4 * self.Input.TunnelCrossSection) + (35 + 0.65 * self.Input.TunnelCrossSection))/2

        self.ScaleTime = self.ScaleTime*(0.57+0.085*self._DrillLength)
        self.TotalCycTime = self.ScaleTime

    def Refresh(self):
        super().Refresh()
        self._DrillLength = self.Input.RoundLength * (1 + self.Input.BlastOverDrill / 100.0)
        if self.Input.Blastability=="Good":
            self.ScaleTime = 6 + 0.4 * self.Input.TunnelCrossSection
        elif self.Input.Blastability=="Poor":
            self.ScaleTime = 35 + 0.65 * self.Input.TunnelCrossSection
        else:
            self.ScaleTime = ((6 + 0.4 * self.Input.TunnelCrossSection) + (35 + 0.65 * self.Input.TunnelCrossSection))/2

        self.ScaleTime = self.ScaleTime*(0.57+0.085*self._DrillLength)
        self.TotalCycTime = self.ScaleTime


class MuckCycleTime(BaseCycleTime):
    def __init__(self, cycinput:CycleInput):
        super().__init__(cycinput)
        self.MoveInSetup = 15  # input calibration needed
        self.Mucking = 60*self.Input.TunnelCrossSection*(1+self.Input.AveOverBreak/100)*self.Input.RoundLength/self.Input.LoaderProductionRate
        self.LossTime = 0.111*(self.MoveInSetup+self.Mucking)
        self.TotalCycTime = self.MoveInSetup + self.Mucking + self.LossTime

    def Refresh(self):
        super().Refresh()
        self.MoveInSetup = 15  # input calibration needed
        self.Mucking = 60*self.Input.TunnelCrossSection*(1+self.Input.AveOverBreak/100)*self.Input.RoundLength/self.Input.LoaderProductionRate
        self.LossTime = 0.111*(self.MoveInSetup+self.Mucking)
        self.TotalCycTime = self.MoveInSetup + self.Mucking + self.LossTime


class SurveyMappingCycleTime(BaseCycleTime):
    def __init__(self, cycinput:CycleInput):
        super().__init__(cycinput)
        self.SurveyMapping = 25
        self.TotalCycTime = self.SurveyMapping

    def Refresh(self):
        super().Refresh()
        self.TotalCycTime = self.SurveyMapping


class SupportCycleTime(BaseCycleTime):
    def __init__(self, cycinput:CycleInput):
        super().__init__(cycinput)
        self.DrillMoveInSetup = 10
        numholes = self.Input.BoltQuantity*self.Input.RoundLength
        self.RBHoleBlow = 0.75 # min
        self.RBInstallTeam = 2
        self.RBDrillBoom = 2
        self.RBLength = 4
        self.RBInstallTimePerMeter = 1.74
        self.RBDrillSpeed = (0.0143*self.Input.DRI+0.8143)  # meter

        self.SCSpraySpeed = 7.64 # m3/hr

        self.BlowAlign4Next =  numholes * self.RBHoleBlow / self.RBDrillBoom
        self.DrillHoles = numholes * self.RBLength / self.RBDrillSpeed / self.RBDrillBoom
        self.InstallRockbolts = numholes * self.RBLength * self.RBInstallTimePerMeter / self.RBInstallTeam

        self.SetupSC = 10 # min pure input
        self.SpraySC = self.Input.SCQuantity * self.Input.RoundLength *60 / self.SCSpraySpeed
        self.CleanupSC = 10 # min pure input

        self.TotalCycTime = self.BlowAlign4Next + self.DrillHoles + self.InstallRockbolts + self.SetupSC + self.SpraySC + self.CleanupSC

    def Refresh(self):
        super().Refresh()
        numholes = self.Input.BoltQuantity*self.Input.RoundLength
        self.RBDrillSpeed = (0.0143*self.Input.DRI+0.8143)  # meter

        self.BlowAlign4Next =  numholes * self.RBHoleBlow / self.RBDrillBoom
        self.DrillHoles = numholes * self.RBLength / self.RBDrillSpeed / self.RBDrillBoom
        self.InstallRockbolts = numholes * self.RBLength * self.RBInstallTimePerMeter / self.RBInstallTeam

        self.SpraySC = self.Input.SCQuantity * self.Input.RoundLength *60 / self.SCSpraySpeed

        self.TotalCycTime = self.BlowAlign4Next + self.DrillHoles + self.InstallRockbolts + self.SetupSC + self.SpraySC + self.CleanupSC


def test():
    cycinput = CycleInput()
    cycinput.UseCatridge = False
    cycinput.Blastability = 'Medium'
    cycinput.Refresh()
    drillcyc = DrillingCycleTime(cycinput)
    blastcyc = BlastingCycleTime(cycinput)
    scalecyc = ScalingCyCleTime(cycinput)
    muckcyc = MuckCycleTime(cycinput)
    sptcyc = SupportCycleTime(cycinput)

    print (cycinput._ExplosivePerRound)
    assert round(cycinput._ExplosivePerRound) == 357
    assert round(cycinput.LoaderProductionRate) == 159
    #print('move in: ',drillcyc.DrillMoveInTime)
    #print('move for next: ',drillcyc.MoveAlign4Next)
    #print('drill burncut: ',drillcyc.DrillBurnCutHole)
    #print('drill blasthole: ',drillcyc.DrillBlastHole)
    #print('change bit: ',drillcyc.ChangeBit)
    #print('lost time: ',drillcyc.LostTime)
    #rint('tot: ',drillcyc.TotalCycleTime)

    print('charge hole fixed time: ', blastcyc.ChargeHoleFixedTime)
    print('charge hold dep time', blastcyc.ChargeHoleLenDepTime)
    print('stem time', blastcyc.StemmingTime)
    print('wire up time', blastcyc.WireUpTime)
    print('tot time: ', blastcyc.TotalCycleTime)

    print('scale time: ', scalecyc.ScaleTime)
    print('')
    print('loader production: ',muckcyc.Input.LoaderProductionRate)
    print('muck time: ', muckcyc.TotalCycTime)
    print('support time: ',sptcyc.TotalCycTime)

    print('pass')

if __name__ == "__main__":
    test()
