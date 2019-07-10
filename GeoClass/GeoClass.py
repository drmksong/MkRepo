import os
import sys
import math
import re
import string
import kivy
import enum


class GeoClassType(enum.Enum):
    gcNone = -1
    gcRMR = 0
    gcQ = 1


class GeoClass:
    def __init__(self,gc):
        self.GeoClassType = gc
        self.RMR = RMR()
        self.Qsys = Qsys()

    def getclass(self):
        if self.GeoClassType == GeoClassType.gcQ:
            return self.Qsys.getclass()
        elif self.GeoClassType == GeoClassType.gcRMR:
            return self.RMR.getclass()
        else:
            return None


class JointCondition(enum.Enum):
    jcVeryGood = 5
    jcGood = 4
    jcFair = 3
    jcPoor = 2
    jcVeryPoor = 1
    jcNone = 0


class RockStrengthType(enum.Enum):
    rsNone = 0
    rsUCS = 1
    rsPointLoad = 2


class RMR:
    def __init__(self):
        self.UCS = 0
        self.pointLoad = 0
        self.rockStrengthType = RockStrengthType.rsNone
        self.RQD = 0
        self.jointSpacing = 0  # meter
        self.jointCondition = JointCondition.jcNone
        self.waterCondition = 0
        self.jointOrientation = 0
        self.rmrValue = -1
        self.geoclass = -1
        self.qValue = -1
        self.isClassified = False

    def getclass(self):
        return self.classify()

    def classify(self):
        self.rmrValue = 0;
        if self.rockStrengthType == RockStrengthType.rsNone:
            self.isClassified = False
            return False

        if self.jointCondition == JointCondition.jcNone:
            self.isClassified = False
            return False

        if self.rockStrengthType == RockStrengthType.rsUCS:
            if self.UCS >= 10:
                self.rmrValue += 5
            elif 5 <= self.UCS < 10:
                self.rmrValue += 4
            elif 1 <= self.UCS < 5:
                self.rmrValue +=3

        if 0 <= self.rmrValue < 20:
            self.geoclass = 5
        elif 20 <= self.rmrValue < 40:
            self.geoclass = 4
        elif 40 <= self.rmrValue < 60:
            self.geoclass = 3
        elif 60 <= self.rmrValue < 80:
            self.geoclass = 2
        elif 80 <= self.rmrValue <= 100:
            self.geoclass = 1
        else:
            self.geoclass = -1

        return self.geoclass




    def conv_to_q(self):
        if self.isClassified:
            self.qValue = math.exp((self.rmrValue - 44)/9)
            return qValue;


class Qsys:
    def __init__(self):
        pass


def test():
    rmr = RMR()
    rmr.rockStrengthType = RockStrengthType.rsUCS
    rmr.UCS = 100

    rmr.RQD = 50
    rmr.jointSpacing = 2
    pass


if __name__ == "__main__":
    test()

