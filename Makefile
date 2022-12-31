.PHONY: pose_estimation
pose_estimation:
	python3 pose_estimation.py -k calibration_matrix.npy -d distortion_coefficients.npy --type DICT_APRILTAG_16h5