import numpy as np


class RelPoseTrans:
    def __init__(self, phi):
        self.phi = phi
    
    def transRelPose(self, pose):
        dist = pose[1]
        pose[1] = dist * np.cos(self.phi)
        pose[2] = (dist**2 - pose[1]**2)**(0.5) + pose[2]

        return pose


def test():
    adj = RelPoseTrans(np.pi/6)
    print(adj.transRelPose([0, 1, 1]))

if __name__ == "__main__":
    test()