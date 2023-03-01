import cv2

import numpy as np
from interp import interpCone
from interp import interpCube

height = 750
width = 100

def transposeCenter(x, y):
	return (x - width//2, -y + height//2)

def detectCone(src, aprilPos):
	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
	lower_yellow = np.array([20, 68, 100]) #hsv
	upper_yellow = np.array([25, 255, 255]) #hsv
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

	result = cv2.bitwise_and(src, src, mask = mask)
	result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	contours = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	contours = contours[0] if len(contours) == 2 else contours[1]
	centers = (0, 0)
	area = 0
	largestAreas = []
	largestPoses = []
	sizeThreshold = 3200
	for contour in contours:

		x,y,w,h = cv2.boundingRect(contour)

		cv2.rectangle(result, (x,y), (x + w, y + h), (255, 0, 0), 4)

		cx = x + w // 2
		cy = y + h // 2
		currArea = w * h
		if (currArea > sizeThreshold):
			largestAreas.append(currArea)
			largestPoses.append((cx, cy))


		if (currArea > area):
			centers= transposeCenter(cx, cy)
	for i in range(len(largestAreas)):
		#aspecRatio 25:18
		#xAngle = (xPos / 1000) * (hFov / 2)
		#yAngle = (yPos / 720) * (vFov / 2)
		angleZ = (largestPoses[i][0] / 1000) * (63.299 / 2)
		angleX = (largestPoses[i][1] / 720) * (45.575 / 2)
		angleX = (2 * angleX) - 22.785 #aply offset
		angleX *= -1
		angleZ = (2 * angleZ) - 30 #apply offset
		distance = interpCone(largestAreas[i])
		radX = angleX * (np.pi/180)
		radZ = angleZ * (np.pi/180)
		yPos = np.sin(radX) * distance * np.sin(radZ) #l/r
		xPos = np.cos(radX) * distance #depth
		zPos = np.sin(radX) * distance * np.cos(radZ) #height
	
		pos = np.array([xPos, yPos, zPos])
		relativePos = pos - np.array([aprilPos[0], aprilPos[1], aprilPos[2]]) # relative pos to cone
		#print(f'relativePos: {relativePos}')
		#print(f'largestArea: {largestArea}')
		#print(f'distance: {interpCone(largestArea)} at: {largestArea} angle ({angleX}, {angleY})                ', end='\r')
		#print(f'angle: ({angleX}, {angleZ})')
		#print(f'position: {pos}')
	'''
	105000 - 0.5m
	50000 - 0.75m
	28000- 1m
	18000 - 1.25m
	12700 - 1.5m
	9300 - 1.75m
	7400 - 2m
        5800 - 2.25m
        4300 - 2.5m
        4000 - 2.75m
        3200 - 3m
	'''
	#print(centers)

	return result

def detectCube(src, aprilPos):
	lower_purple = np.array([117, 85, 65]) #hsv
	upper_purple = np.array([130, 255, 255]) #hsv
	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_purple, upper_purple)

	result = cv2.bitwise_and(src, src, mask = mask)
	result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	contours = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	contours = contours[0] if len(contours) == 2 else contours[1]
	centers = (0, 0)
	area = 0
	largestAreas = []
	largestPoses = []
	sizeThreshold = 3300
	for contour in contours:

		x,y,w,h = cv2.boundingRect(contour)

		cv2.rectangle(result, (x,y), (x + w, y + h), (255, 0, 0), 4)

		cx = x + w // 2
		cy = y + h // 2
		currArea = w * h
		if (currArea > sizeThreshold):
			largestAreas.append(currArea)
			largestPoses.append((cx, cy))


		if (currArea > area):
			centers= transposeCenter(cx, cy)
	for i in range(len(largestAreas)):
		#aspecRatio 25:18
		#xAngle = (xPos / 1000) * (hFov / 2)
		#yAngle = (yPos / 720) * (vFov / 2)
		angleZ = (largestPoses[i][0] / 1000) * (63.299 / 2)
		angleX = (largestPoses[i][1] / 720) * (45.575 / 2)
		angleX = (2 * angleX) - 22.785 #apply offset
		angleX *= -1
		angleZ = (2 * angleZ) - 30 #apply offset
		distance = interpCube(largestAreas[i])
		radX = angleX * (np.pi/180)
		radZ = angleZ * (np.pi/180)
		yPos = np.sin(radX) * distance * np.sin(radZ) #l/r
		xPos = np.cos(radX) * distance #depth
		zPos = np.sin(radX) * distance * np.cos(radZ) #height
	
		pos = np.array([xPos, yPos, zPos])
		relativePos = pos - np.array([aprilPos[0], aprilPos[1], aprilPos[2]]) # relative pos from apriltag to cube
		#print(f'relativePos: {relativePos}')
		#print(f'largestArea: {largestArea}')
		#print(f'distance: {distance}')
		#print(f'distance: {interpCube(largestArea)} at: {largestArea} angle ({angleX}, {angleY})                ', end='\r')
		#print(f'angle: ({angleX}, {angleZ})')
		#print(f'position: {pos}')
	'''
	60000 - .5m
	34900 - .75m0287106 -0.02248793]
position: [ 2.84985788  0.
	21000 - 1m
	14000 - 1.25m
	9000 - 1.5m
	8000 - 1.75m
	6500 - 2m
	5700 - 2.25m
	4200 - 2.5m
	4000 - 2.75
0287106 -0.02248793]
position: [ 2.84985788  0.	3300 - 3m
	'''
	#print(centers)

	return result
