from json import loads
import numpy as np

class FieldTag:
    def __init__(self, x, y, offset):
        self.x = x
        self.y = y
        self.offset = offset

    def calcAbsPose(self, other):
        rotMat = np.array([
            [np.cos(self.orientation), -np.sin(self.orientation), 0],
            [np.sin(self.orientation), np.cos(self.orientation), 0],
            [0, 0, 1]
        ])

        transMat = np.array([
            [1, 0, self.x],
            [0, 1, self.y],
            [0, 0, 1],
        ])

        return rotMat * transMat * other


class Field:
    def __init__(self, filePath):
        self.filePath = filePath
        self.matMap = {}
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

    def adjustPose(self, pose, tagVal):
        return self.matMap[tagVal].calcAbsPose(pose)

def parseLine(line, matMap):
    if line[0] == "tagNum":
        tagNum = int(line[1])
    elif line[0] == "x":
        x = int(line[1])
    elif line[0] == "y":
        y = int(line[1])
    elif line[0] == "offset":
        offset = int(offset)
    else:
        matMap[tagNum] = FieldTag(x, y, offset)
    
    return matMap
