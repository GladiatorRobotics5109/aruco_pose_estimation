from json import loads
import numpy as np
import os
from fieldTag import FieldTag

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
            z = None
            offset = None
            for line in lines:
                line = line.split(":")

                if len(line) == 2:
                    self.matMap = parseLine(line, self.matMap)
    
    def getAbsPose(self, poses, angOffset):
        absCoord = np.array([
            0.0,
            0.0,
            0.0,
            1.0
        ])

        for tagVal, pose in poses:
            try:
                print(np.shape(self.matMap[tagVal].calcAbsPose(pose, angOffset)))
                print(np.shape(absCoord))
                absCoord += self.matMap[tagVal].calcAbsPose(pose, angOffset)
            except Exception as e:
                print(e)
                print("Tag not in dict")

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
    elif line[0] == "z":
        z = int(line[1])
    elif line[0] == "tagMapPath":
        matmMap[tagNum] = FieldTag(tagNum, offset, matPath=line[1])
    else:
        matMap[tagNum] = FieldTag(tagNum, offset, x, y, z)
    
    return matMap
