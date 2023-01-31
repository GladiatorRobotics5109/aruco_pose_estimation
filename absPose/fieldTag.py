from json import loads
import numpy as np
import os

class FieldTag:
    def __init__(self, matId, theta, x=None, y=None, z=None, matPath=None):
        self.initialized = False
        self.matId = matId
        self.calcedMat = None
        self.theta = theta
        if (x != None):
            # Clockwise rotation matrix
            rotMat = np.array([
                [np.cos(theta), np.sin(theta), 0, 0],
                [-np.sin(theta), np.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

            # Translation matrix
            transMat = np.array([
                [1, 0, 0, x],
                [0, 1, 0, y],
                [0, 0, 1, z],
                [0, 0, 0, 1]
            ])

            self.calcedMat = np.matmul(rotMat, transMat)
        else:
            self.calcedMat = numpy.load(matPath)

    
    def calcAbsPose(self, other, angOffset):

        # adjust for angle offset
        diff = angOffset - self.theta

        transMat = np.array([
            [np.cos(diff), -np.sin(diff), 0, 0],
            [np.sin(diff), np.cos(diff), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        other = transMat.dot(other)
        other = np.transpose(other)
        # Returns projection of vector onto actual field
        final = self.calcedMat.dot(other)
        print(final)
        return final

    def __del__(self):
        if (not os.path.exists("./tags_npy/")):
            os.mkdir("./tags_npy/")
        np.save(f"./tags_npy/tag_{self.matId}.npy", self.calcedMat)




def test():
    tag = FieldTag(1, np.pi/2, 0, 2, 2)

    print(tag.calcAbsPose([[1], [1], [-1], [1]], np.pi/2))

if __name__ == "__main__":
    test()
