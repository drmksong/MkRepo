import pykrige
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
import kivy
import numpy as np


class GeoModel:
    def __init__(self):
        self.FileName = ""
        self.Data = np.array([[]])

    def load(self, fname):
        self.FileName = fname
        self.Data = np.array([[0,0,0,0]])
        with open(fname, 'r') as f:
            lines = f.readlines()
        for line in lines:
            numbers = line.split()

            #x,y,z,v = numbers
            #print (numbers)
            x = numbers[0]
            y = numbers[1]
            z = numbers[2]
            v = numbers[3]
            #print(x,y,z,v)
            self.Data = np.append(self.Data,[[x,y,z,v]],axis = 0)

        self.Data = np.delete(self.Data,0,axis=0)
        print(self.Data)

    def getvalue(self,x,y,z):
        return 100

    def getclass(self,x,y,z):
        cl = -1
        value = self.getvalue(x,y,z)
        if value < 20:
            cl = 5
        elif 20 <= value < 40:
            cl = 4
        elif 40 <= value < 60:
            cl = 3
        elif 60 <= value < 80:
            cl = 2
        elif 80 <= value <= 100:
            cl = 1
        return cl


def test():
    data = np.array([[0,0,0,0]])
    data = np.append(data,[[1,2,3,4]],axis = 0)
    data = np.append(data,[[2,3,4,5]],axis = 0)
    data = np.delete(data,0,axis=0)
    print (data)
    gm = GeoModel()
    gm.load("hslpg.txt")



'''
    data = np.array([[0.3, 1.2, 0.47],
                     [1.9, 0.6, 0.56],
                     [1.1, 3.2, 0.74],
                     [3.3, 4.4, 1.47],
                     [4.7, 3.8, 1.74]])
    gridx = np.arange(0.0, 5.5, 0.5)
    gridy = np.arange(0.0, 5.5, 0.5)
    # Create the ordinary kriging object. Required inputs are the X-coordinates of
    # the data points, the Y-coordinates of the data points, and the Z-values of the
    # data points. If no variogram model is specified, defaults to a linear variogram
    # model. If no variogram model parameters are specified, then the code automatically
    # calculates the parameters by fitting the variogram model to the binned
    # experimental semivariogram. The verbose kwarg controls code talk-back, and
    # the enable_plotting kwarg controls the display of the semivariogram.
    OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
                         verbose=False, enable_plotting=False)
    # Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
    # grid of points, on a masked rectangular grid of points, or with arbitrary points.
    # (See OrdinaryKriging.__doc__ for more information.)
    z, ss = OK.execute('grid', gridx, gridy)
    # Writes the kriged grid to an ASCII grid file.
    kt.write_asc_grid(gridx, gridy, z, filename="output.asc")

    for zv in z:
        print (zv)
'''

if __name__ == "__main__":
    test()



