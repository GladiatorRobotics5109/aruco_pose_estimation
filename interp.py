import numpy

yVal = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
xValCone = [105000, 50000, 28000, 18000, 12700, 9300, 7400, 5800, 4300, 4000, 3200]

xValCube =[60000, 34900, 21000, 14000, 9000, 8000, 6500, 5700, 4200, 4000,3300]


xValCone = xValCone[::-1]
xValCube = xValCube[::-1]
yVal = yVal[::-1]

def interpCone(evalTarget):
	dist = numpy.interp(evalTarget, xValCone, yVal)
	#check if we need to extrapolate
	#if (dist == yVal[0]:
	return dist

def interpCube(evalTarget):
        dist = numpy.interp(evalTarget, xValCube, yVal)
        return dist

