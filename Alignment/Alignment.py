import math
import sys
import os
import string
import re

class Point:
    def __init__(self, x,y,z):
        self.X = x
        self.Y = y
        self.Z = z

    def CalcDist(self, pnt):
        dis = math.sqrt(math.pow(pnt.X - self.X,2)+math.pow(pnt.Y - self.Y,2)+math.pow(pnt.Z - self.Z,2))
        return dis


class WorkingPoint:
    pass


class Tunnel:
    pass


def test():
    p1 = Point(1,2,3)
    p2 = Point(4,5,6)
    d = Point.Dist(p1,p2)

    assert d==5

    print pass


if __name__ == "__main__":
    test()