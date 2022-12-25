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
        with open(filePath) as f:
            self.matMap = loads(f.read())

    def adjustPose(self, pose, tagVal):
        return self.matMap[tagVal].calcAbsPose(pose)
