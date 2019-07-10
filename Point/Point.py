import math


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


def test():
    p1 = Point(0, 0, 0)
    p2 = Point(0, 1, 0)
    p3 = Point(0, 2, 0)
    p4 = Point(1, 2, 0)

    ps = [p1, p2, p3, p4]

    pnts = Points(ps)

    d = p1.calc_dist(p2)
    print(d)
    pnts.print()

    wp = WorkingPoints(pnts)
    wp.setpoints(pnts)

    wp.print()
    wp[0].print()
    assert wp[0].X == 0
    print('pass')


if __name__ == "__main__":
    test()
