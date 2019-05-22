import os
import sys
import math
import re
import string
import kivy
import enum


class rbType(enum.Enum):
    rbSteelBar = 0
    rbFRP = 1
    rbSteelShell = 2


class Rockbolt:
    def __init__(self):
        self.diameter = 0
        self.length = 0
        self.density = 0 # area per rockbolt
        self.material = rbType.rbSteelBar


class scType(enum.Enum):
    scNormal = 0
    scSFRC = 1


class Shotcrete:
    def __init__(self):
        self.thickness = 0
        self.type = scType.scNormal


class RockSupport:
    def __init__(self):
        self.rockbolt = Rockbolt()
        self.shotcrete = Shotcrete()
        pass


def test():
    pass


if __name__ == "__main__":
    test()

