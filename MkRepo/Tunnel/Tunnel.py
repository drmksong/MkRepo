import sys
sys.path.append("..")

from Point.Point import Point as PT
from Point.Point import Points as PTS
from Point.Point import WorkingPoints as WPS

class Tunnel:
    def __init__(self,wp): # sp and ep are not points but index to the points
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
        self.Length = -1

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

    def calc_length(self):
        if self.StartPoint==-1 or self.EndPoint == -1:
            return 0
        self.Length = self.WorkingPoints[self.StartPoint].calc_dist(self.WorkingPoints[self.EndPoint])
        return self.Length

    def station(self, dis):
        sp = self.WorkingPoints[self.StartPoint]
        ep = self.WorkingPoints[self.EndPoint]
        A = ep.X - sp.X
        B = ep.Y - sp.Y
        C = ep.Z - sp.Z

        dist = self.calc_length()

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
        length = self.calc_length()

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

    def excav(self):
        pass

    def __getitem__(self, item):
        return self.Tunnels[item]

    def __setitem__(self, key, value):
        self.Tunnels[key] = value

def test():

    pnt1 = PT(0,0,0)
    pnt2 = PT(1,0,0)
    pnt3 = PT(2,0,0)

    pnts = PTS([pnt1,pnt2,pnt3])
    wps = WPS(pnts)
    tun1 = Tunnel(wps)
    tun2 = Tunnel(wps)

    tun1.setwp(0,1)
    tun2.setwp(1,2)
    tuns = Tunnels([tun1, tun2])

if __name__ == "__main__":
    test()
