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

    def calcDist(self, pnt):
        dis = math.sqrt(math.pow(pnt.X - self.X,2)+math.pow(pnt.Y - self.Y,2)+math.pow(pnt.Z - self.Z,2))
        return dis

    def print(self):
        print("pnt: X ",self.X,", Y ",self.Y,", Z ",self.Z)


class WorkingPoints:
    def __init__(self,pnts):
        self.Points = []
        for pnt in pnts:
            self.Points.append(pnt)

    def add(self,pnt):
        self.Points.append(pnt)

    def size(self):
        return len(self.Points)

    def print(self):
        for pnt in self.Points:
            pnt.print()


class Tunnel:
    def __init__(self,wp): # sp and ep are not points but index to the points
        self.WorkingPoints = wp
        self.StartPoint = -1
        self.EndPoint = -1

    def setWP(self,sp,ep):
        self.StartPoint = sp
        self.EndPoint = ep


class Tunnels:
    def __init__(self,tuns):
        self.Tunnels = []
        for tun in tuns:
            self.Tunnels.append(tun)


def test():
    p1 = Point(1,1,1)
    p2 = Point(1,1,2)
    pnts = [p1,p2]
    d = p1.calcDist(p2)
    wp = WorkingPoints(pnts)
    wp.print()
    assert wp.size() == 2
    assert d==1


    print ("pass")


if __name__ == "__main__":
    test()