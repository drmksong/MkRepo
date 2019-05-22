import math
import sys
import os
import string
import re
import kivy


class Alignment:
    def __init__(self):
        self.FileName = ""
        self.WorkingPoints = WorkingPoints([])
        self.Tunnels = Tunnels([])

    def load(self,fname):
        self.FileName = fname
        with open(fname,'r') as f:
            lines = f.readlines()
        for line in lines:
            print(line,end=' ')

# TODO: implement the saving function
    def save(self,fname):
        pass


class Point:
    def __init__(self, x,y,z):
        self.X = x
        self.Y = y
        self.Z = z

    def calc_dist(self, pnt):
        dis = math.sqrt(math.pow(pnt.X - self.X,2)+math.pow(pnt.Y - self.Y,2)+math.pow(pnt.Z - self.Z,2))
        return dis

    def print(self):
        print("pnt: X ",self.X,", Y ",self.Y,", Z ",self.Z)


class WorkingPoints:
    def __init__(self,pnts):
        self.Points = []
        for pnt in pnts:
            self.Points.append(pnt)

    def append(self,pnt):
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

    def calc_dist(self):
        if self.StartPoint==-1 or self.EndPoint == -1:
            return 0
        return self.WorkingPoints.Points[self.StartPoint].calc_dist(self.WorkingPoints.Points[self.EndPoint])

    def station(self, dis):

        sp = self.WorkingPoints.Points[self.StartPoint]
        ep = self.WorkingPoints.Points[self.EndPoint]
        A = ep.X - sp.X
        B = ep.Y - sp.Y
        C = ep.Z - sp.Z

        dist = self.calc_dist()

        t = dis/dist

        if t > 1.0:
            print("t is greater than 1.0")

        pnt = Point(0,0,0)
        pnt.X = sp.X + A * t
        pnt.Y = sp.Y + B * t
        pnt.Z = sp.Z + C * t

#        print (pnt.X, pnt.Y, pnt.Z, A, B, C, t)
        return pnt


class Tunnels:
    def __init__(self,tuns):
        self.Tunnels = []
        for tun in tuns:
            self.Tunnels.append(tun)

    def size(self):
        return len(self.Tunnels)

    def append(self,tun):
        self.Tunnels.append(tun)


def test():
    p1 = Point(1,1,1)
    p2 = Point(1,1,2)
    p3 = Point(1,1,3)
    p4 = Point(1,1,4)

    pnts = list()
    pnts.append(p1)
    pnts.append(p2)
    pnts.append(p3)
    d = p1.calc_dist(p2)
    wp = WorkingPoints(pnts)
    wp.append(p4)
    wp.print()
    t1 = Tunnel(wp)
    t2 = Tunnel(wp)

    t1.setWP(0,2)
    t2.setWP(2,1)

    tuns = Tunnels([])
    tuns.append(t1)
    tuns.append(t2)

    d2 = t1.calc_dist()
    d3 = t2.calc_dist()
    pnt = t1.station(1)

    align = Alignment()
    align.load("1.txt")

    assert wp.size() == 4
    assert d == 1
    assert d2 == 2
    assert d3 == 1
    assert pnt.Z == 2
    assert tuns.size() == 2

    print ("pass")


if __name__ == "__main__":
    test()