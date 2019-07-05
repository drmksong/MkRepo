import math
import sys
import os
import string
import re
#import kivy
import time

from datetime import date as dt
import enum
import copy
from colorama import Fore
from colorama import Style

from GeoClass.GeoClass import GeoClass
from GeoClass.GeoClass import GeoClassType
from GeoModel.GeoModel import GeoModel
from CycleTime.CycleTime import Cycles


class Alignment:
    def __init__(self):
        self.FileName = ""
        self.WorkingPoints = WorkingPoints([])
        self.Tunnels = Tunnels([])
        self.Portals = []

    def load(self,fname):
        self.FileName = fname
        with open(fname,'r') as f:
            lines = f.readlines()

        line = lines[0]
        print (line)
        cnt = 1
        cols = line.split(' ')
        np = int(cols[0])
        pnts = Points([])

        for i in range(np):
            line = lines[cnt]
            cols = line.split(' ')
            print(f'x,y,z {Fore.GREEN} ', (cols[0]), (cols[1]), (cols[2]), f'{Style.RESET_ALL}')
            x, y, z = float(cols[0]), float(cols[1]), float(cols[2])
            wp = Point(x,y,z)
            pnts.append(wp)
            cnt += 1

        self.WorkingPoints.setpoints(pnts)
        self.WorkingPoints.size()
        self.WorkingPoints.print()

        line = lines[cnt]
        cols = line.split(' ')
        nt = int(cols[0])
        cnt += 1

        for i in range(nt):
            line = lines[cnt]
            cols = line.split(' ')
            s, e = int(cols[0]), int(cols[1])
            tun = Tunnel(self.WorkingPoints)
            tun.StartPoint = s
            tun.EndPoint = e
            self.Tunnels.append(tun)
            cnt += 1

        line = lines[cnt]
        cols = line.split(' ')
        np = int(cols[0])
        cnt += 1

        for i in range(np):
            line = lines[cnt]
            cols = line.split(' ')
            p = int(cols[0])
            self.Portals.append(p)
            cnt += 1

    # TODO: implement the saving function
    def save(self, fname):
        pass








def test():

    p1 = Point(0, 0, 0)
    p2 = Point(0, 1, 0)
    p3 = Point(0, 2, 0)
    p4 = Point(1, 2, 0)

    ps = [p1, p2, p3, p4]

    pnts = Points(ps)

    #pnts.append(p1)
    #pnts.append(p2)
    #pnts.append(p3)
    d = p1.calc_dist(p2)
    print(d)
    pnts.print()

    wp = WorkingPoints(pnts)
    wp.setpoints(pnts)
    #wp.append(p4)
    wp.print()
    wp[0].print()

    t1 = Tunnel(wp)
    t2 = Tunnel(wp)

    t1.setwp(0,2)
    t2.setwp(2,1)

    exf = ExcavFace()
    exf.set(0,ExcavDir.edForward,2,dt.today())
    exf2 = ExcavFace()
    exf2.set(2,ExcavDir.edForward,4,dt.today())

    efs = ExcavFaces([])
    efs.append(exf)
    efs.append(exf2)
    efs.print()

    t1.excav()

    tun_list = [t1,t2]

    tuns = Tunnels(tun_list)
#   tuns.append(t1)
#   tuns.append(t2)

    tuns.excav()


    tuns[0].print()

    d2 = t1.calc_length()
    d3 = t2.calc_length()
    pnt = t1.station(1)

    align = Alignment()
    align.load("Alignment/1.txt")

    assert wp.size() == 4
    assert d == 1
    assert d2 == 2
    assert d3 == 1
    print (pnt.X, pnt.Y, pnt.Z)
    assert pnt.Z == 0
    assert tuns.size() == 2
    print (align.WorkingPoints.size())
    assert align.WorkingPoints.size() == 8
    assert align.Tunnels.size() == 12
    assert len(align.Portals) == 1

    sts = align.Tunnels[0].trace()
    for st in sts:
        print(st.X, st.Y, st.Z)

    print ("pass")





if __name__ == "__main__":
    test()
