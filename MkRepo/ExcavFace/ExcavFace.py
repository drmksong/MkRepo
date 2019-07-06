import sys
sys.path.append("..")

import enum
import copy
from datetime import date as dt
from GeoClass.GeoClass import GeoClassType
from GeoClass.GeoClass import GeoClass


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

    def setcoord(self ,x ,y ,z):
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
    def __init__(self,faces: [ExcavFace]):
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



def test():
    face1 = ExcavFace()
    face2 = ExcavFace()
    face1.set(1,ExcavDir.edForward,1,dt.today())
    face1.set(1,ExcavDir.edForward,1,dt.today())
    faces = ExcavFaces([face1,face2])


if __name__ == "__main__":
    test()
