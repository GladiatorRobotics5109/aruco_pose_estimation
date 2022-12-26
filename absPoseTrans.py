from json import loads
import numpy as np

class FieldTag:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def calcAbsPose(self, other):

        # Clockwise rotation matrix
        rotMat = np.array([
            [np.cos(self.theta), np.sin(self.theta), 0],
            [-np.sin(self.theta), np.cos(self.theta), 0],
            [0, 0, 1]
        ])

        # Translation matrix
        transMat = np.array([
            [1, 0, self.x],
            [0, 1, self.y],
            [0, 0, 1],
        ])
        
        # Returns projection of vector onto actual field
        return np.matmul(rotMat, transMat).dot(other)


class Field:
    def __init__(self, filePath=None, tagPose=None):
        self.filePath = filePath
        self.matMap = {}
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
    def getAbsPose(self, pose, tagVal):
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



def test():
    tag = FieldTag(0, 2, np.pi/4)

    print(tag.calcAbsPose([[1], [1], [1]]))

if __name__ == "__main__":
    test()