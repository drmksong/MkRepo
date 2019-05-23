import os
import sys
import math
import re
import string
import kivy
import enum


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
        self.qValue = -1
        self.isClassified = False

    def classify(self):
        if self.rockStrengthType == RockStrengthType.rsNone:
            self.isClassified = False
            return -1

        if self.jointCondition == JointCondition.jcNone:
            self.isClassified = False
            return -1

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

