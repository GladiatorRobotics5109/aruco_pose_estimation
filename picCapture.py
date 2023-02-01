import cv2

cam = cv2.VideoCapture("/dev/video0")
width=1000
counter = 0

while (True):
    ret, frame = cam.read()

    if (ret):
        cv2.imshow("view", frame)
        h, w, _ = frame.shape

        key = cv2.waitKey(1)
        height = int(width*(h/w))
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

        if ord("c") == key:
            cv2.imwrite(f"./targets/img{counter}.jpg", frame)
            counter += 1
        elif ord("q") == key:
            break
