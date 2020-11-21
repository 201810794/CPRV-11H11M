import cv2
import time
import numpy as np

scale = 2
cap = cv2.VideoCapture(0)

list_eye_locaton = []
history_eye_locations = []
isDraw = True

white = cv2.imread('./white.png')

while True:

    ret, frame = cap.read()
    #frame = cv2.flip(frame, 1)

    height, width, channels = frame.shape

    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    roi = resized_cropped
    roi = cv2.flip(roi, 1)
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi,(7,7),0)

    _, threshold = cv2.threshold(gray_roi,28,255,cv2.THRESH_BINARY_INV)
    contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    whiteImg = cv2.addWeighted(roi, 0, white, 100, 0)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cenX = int((x + (x+w)) / 2)
        cenY = int((y + (y+h)) / 2)
        cv2.circle(whiteImg, (cenX, cenY), 10, (0, 255, 0), -1)

        break

    cv2.putText(whiteImg, str(15), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0))

    cv2.imshow("Bin", threshold)
    cv2.imshow("Gray ROI", gray_roi)
    cv2.imshow("Eye tracking", whiteImg)
    key = cv2.waitKey(1)
    if key == 27: #esc
        break

    '''
    elif key == 32: #space bar
        list_eye_locaton.clear()
        history_eye_locations.clear()
    elif key == ord('v'):
        isDraw = not isDraw
    '''

cv2.destroyAllWindows()