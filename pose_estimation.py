'''
Sample Usage:-
python pose_estimation.py --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
'''


import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time
from networktables import NetworkTables

sys.path.append("./absPose")

from relPoseTrans import RelPoseTrans
from field import Field

ip = "10.51.9.2"
theta = np.pi / 6

field = Field(matMap={})


def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients)

        # If markers are detected
    tvecs = []
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.1, matrix_coefficients,
                                                                       distortion_coefficients)
            tvecs.append([tvec, ids[i]])
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners) 

            # Draw Axis
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  

    return frame, tvecs

if __name__ == '__main__':
    NetworkTables.initialize(server=ip)
    sd = NetworkTables.getTable("SmartDashboard")
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--K_Matrix", required=True, help="Path to calibration matrix (numpy file)")
    ap.add_argument("-d", "--D_Coeff", required=True, help="Path to distortion coefficients (numpy file)")
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())
    # args["type"] = args["type"].upper()
    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]
    
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    video = cv2.VideoCapture("/dev/video0")
    time.sleep(2.0)

    adj = RelPoseTrans(theta)

    while True:
        ret, frame = video.read()

       	if not ret:
            break

        h, w, _ = frame.shape

        width=1000
        height = int(width*(h/w))
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
        
        output, tvecs = pose_esitmation(frame, aruco_dict_type, k, d)
	
        cv2.imshow('Estimated Pose', output)
        if len(tvecs) > 0:
            poseMap = [(singId, adj.transRelPose([-tvec[0][0][0], tvec[0][0][1], tvec[0][0][2]]))for tvec, singId in tvecs]
            angle = sd.getNumber("angle", 0)
            sd.putNumberArray("pose", field.getAbsPose(poseMap, angle))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
