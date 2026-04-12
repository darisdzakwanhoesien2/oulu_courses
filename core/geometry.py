import cv2
import numpy as np

def detect_circles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT,
        dp=1, minDist=50,
        param1=150, param2=30,
        minRadius=20, maxRadius=200
    )

    out = img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x,y,r in circles[0]:
            cv2.circle(out, (x,y), r, (255,0,0), 2)
    return out