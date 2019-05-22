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


class RMR:
    def __init__(self):
        self.UCS = 0
        self.pointLoad = 0
        self.RQD = 0
        self.jointSpacing = 0
        self.jointCondition = JointCondition.jcNone
        self.waterCondition = 0
        self.jointOrientation = 0
        self.rockClass = 0

    def classify(self):
        pass


class Qsys:
    def __init__(self):
        pass
