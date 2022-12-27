from json import loads
import numpy as np
import os

class FieldTag:
    def __init__(self, matId, x=None, y=None, theta=None, matPath=None):
        self.initialized = False
        self.matId = matId
        self.calcedMat = None
        if (x != None):
            # Clockwise rotation matrix
            rotMat = np.array([
                [np.cos(theta), np.sin(theta), 0],
                [-np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])

            # Translation matrix
            transMat = np.array([
                [1, 0, x],
                [0, 1, y],
                [0, 0, 1],
            ])

            self.calcedMat = np.matmul(rotMat, transMat)
        else:
            self.calcedMat = numpy.load(matPath)

    
    def calcAbsPose(self, other):
        # Returns projection of vector onto actual field
        return self.calcedMat.dot(other)

    def __del__(self):
        if (not os.path.exists("./tags_npy/")):
            os.mkdir("./tags_npy/")
        np.save(f"./tags_npy/tag_{self.matId}.npy", self.calcedMat)


class Field:
    def __init__(self, filePath=None, tagPose=None):
        self.filePath = filePath
        self.matMap = {}

        # Can use a file or hardocded dictionary
        if (filePath != None):
            self.parseFile(filePath)
        else:
            self.matMap = tagPose

    def parseFile(self, filePath):
        with open(filePath) as f:
            lines = f.readlines()
            tagNum = -1
            x = None
            y = None
            offset = None
            for line in lines:
                line = line.split(":")

                if len(line) == 2:
                    self.matMap = parseLine(line, self.matMap)
    def getAbsPose(self, poses):
        absCoord = np.array([
            [0], 
            [0], 
            [1]
        ])
        
        for tagVal, pose in poses:
            absCoord += self.matMap[tagVal].calcAbsPose(pose)

        return absCoord/len(poses)

def parseLine(line, matMap):
    if line[0] == "tagNum":
        tagNum = int(line[1])
    elif line[0] == "x":
        x = int(line[1])
    elif line[0] == "y":
        y = int(line[1])
    elif line[0] == "offset":
        offset = int(offset)
    elif line[0] == "tagMapPath":
        matmMap[tagNum] = np.load(line[1])
    else:
        matMap[tagNum] = FieldTag(tagNum, x, y, offset)
    
    return matMap



def test():
    tag = FieldTag(1, 0, 2, np.pi/2)

    print(tag.calcAbsPose([[1], [1], [1]]))

if __name__ == "__main__":
    test()