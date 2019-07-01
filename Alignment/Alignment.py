import math
import sys
import os
import string
import re
# import kivy
import time
from GeoClass.GeoClass import GeoClass
from GeoClass.GeoClass import GeoClassType
from GeoModel.GeoModel import GeoModel
from datetime import date as dt
import enum
import copy
from colorama import Fore
from colorama import Style


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


class Points:
    def __init__(self, pnts: [Point]):
        self.Points = []
        for pnt in pnts:
            self.Points.append(pnt)

    def size(self):
        return len(self.Points)

    def append(self, pnt):
        self.Points.append(pnt)

    def print(self):
        for pnt in self.Points:
            print(pnt.X, pnt.Y, pnt.Z)

    def __getitem__(self, item):
        return self.Points[item]

    def __setitem__(self, key, value):
        self.Points[key] = value


class WorkingPoints:
    def __init__(self, pnts: Points):
        self.Points = pnts

    def setpoints(self, pnts): # pnts is Points class
        self.Points = pnts

    def append(self, pnt):
        self.Points.append(pnt)

    def size(self):
        return self.Points.size()

    def print(self):
        self.Points.print()

    def __getitem__(self, item):
        return self.Points[item]

    def __setitem__(self, key, value):
        self.Points[key] = value


class ExcavDir(enum.Enum):
    edNone = -1
    edForward = 0
    edBackward = 1


class ExcavFace:
    def __init__(self):
        self.Location = 0 # in terms of station from start to end
        self.x = -1
        self.y = -1
        self.z = -1
        self.Direction = ExcavDir.edNone
        self.Advance = 0 # advance per blast round
        self.Date = dt(1,1,1)
        self.Excavated = False
        self.Current = False
        self.RockClass = GeoClass(gc=GeoClassType.gcNone)
        self.Round = []

    def set(self, loc, dir: ExcavDir, adv, date):
        self.Location = loc
        self.Direction = dir
        self.Advance = adv
        self.Date = date
        start = loc
        end = loc + adv*(1 if dir == ExcavDir.edForward else -1)
        self.Round = [start, end]

    def setcoord(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def setcurrent(self):
        self.Current = True

    def excav(self):
        self.Excavated = True
        self.Current = False

    def getclass(self):
        self.RockClass = GeoModel.getclass(self.x, self.y, self.z)


class ExcavFaces:
    def __init__(self, faces: [ExcavFace]):
        self.Faces = []
        self.Excavated = []

        for face in faces:
            self.Faces.append(face)

    def size(self):
        return len(self.Faces)

    def append(self, face):
        self.Faces.append(face)
        self.Excavated.append(face.Round)
        self.refresh()

    def remove(self, face):
        self.Faces.remove(face)
        self.Excavated.remove(face.Round)

    def refresh(self):
        exc = copy.copy(self.Excavated)
        for i in range(len(exc)-1):
            if exc[i][1] == exc[i+1][0]:
                self.Excavated.remove(exc[i])
                self.Excavated.remove(exc[i+1])
                self.Excavated.append([exc[i][0], exc[i+1][1]])

    def print(self):
        for face in self.Faces:
            print(face.Location, face.Direction, face.Advance, face.Round)
        print(self.Excavated)

    def __getitem__(self, item):
        return self.Faces[item]

    def __setitem__(self, key, value):
        self.Faces[key] = value


class Tunnel:
    def __init__(self, wp): # sp and ep are not points but index to the points
        self.WorkingPoints = wp
        self.StartPoint = -1
        self.EndPoint = -1
        self.StartExcavFace = ExcavFace()
        self.EndExcavFace = ExcavFace()
        self.ExcavFaces = ExcavFaces([])
        self.Completed = False
        self.Progress = 0 # in percent
        self.Height = -1
        self.Width = -1
        self.Area = -1
        self.Perimeter = -1
        self.CumProd = 0

    def setheight(self,h):
        self.Height = h

    def setwidth(self,w):
        self.Width = w

    def setarea(self,a):
        self.Area = a

    def setperi(self,p):
        self.Perimeter = p

    def setwp(self,sp,ep):
        self.StartPoint = sp
        self.EndPoint = ep

    def calc_dist(self):
        if self.StartPoint==-1 or self.EndPoint == -1:
            return 0
        return self.WorkingPoints[self.StartPoint].calc_dist(self.WorkingPoints[self.EndPoint])

    def station(self, dis):
        sp = self.WorkingPoints[self.StartPoint]
        ep = self.WorkingPoints[self.EndPoint]
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

    def trace(self):
        stations = []
        length = self.calc_dist()

        for i in range(int(length)):
            stations.append(self.station(i))

        for st in stations:
            print(st.X, st.Y, st.Z)

        return stations

    def excav(self):
        faces = copy.copy(self.ExcavFaces.Faces)
        prod = 0
        for face in faces:
            if face.Current == True:
                nf = ExcavFace()
                loc = face.Location + face.Direction*face.Advance
                dir = face.Direction
                adv = face.Advance
                date = dt.today()
                tun = face.Tunnel
                nf.set(loc,dir,adv,date,tun)
                nf.Current = True

                self.ExcavFaces.append(nf)
                face.Current = False
                prod = prod + adv*self.Area

            else:
                pass
        self.CumProd = self.CumProd + prod
        return prod

    def print(self):
        print ('Tunnel::print ',self.StartPoint,self.EndPoint)


class Tunnels:
    def __init__(self,tuns:[Tunnel]):
        self.Tunnels = []
        self.Completed = False
        for tun in tuns:
            self.Tunnels.append(tun)

    def size(self):
        return len(self.Tunnels)

    def append(self,tun):
        self.Tunnels.append(tun)

    def iscompleted(self):
        completed = True
        for tun in self.Tunnels:
            completed = completed and tun.Completed
        self.Completed = completed
        return self.Completed

    def __getitem__(self, item):
        return self.Tunnels[item]

    def __setitem__(self, key, value):
        self.Tunnels[key] = value


def test():
    ps = []

    p1 = Point(1.0,1,1)
    p2 = Point(1,1,2)
    p3 = Point(1,1,3)
    p4 = Point(1,1,4)

    pnts = Points(ps)
    pnts.append(p1)
    pnts.append(p2)
    pnts.append(p3)
    d = p1.calc_dist(p2)
    print(d)
    pnts.print()

    wp = WorkingPoints(pnts)
    wp.setpoints(pnts)
    wp.append(p4)
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

    tuns = Tunnels([])
    tuns.append(t1)
    tuns.append(t2)

    tuns[0].print()

    d2 = t1.calc_dist()
    d3 = t2.calc_dist()
    pnt = t1.station(1)

    align = Alignment()
    align.load("Alignment/1.txt")

    assert wp.size() == 4
    assert d == 1
    assert d2 == 2
    assert d3 == 1
    print (pnt.X, pnt.Y, pnt.Z)
    assert pnt.Z == 2
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
