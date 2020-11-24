import cv2
import time

scale = 2
cap = cv2.VideoCapture(0)

list_eye_locaton = []
history_eye_locations = []
isDraw = True

black = cv2.imread('./black.png')
adv = cv2.imread('./adv.jpg')

TIMER = int(15)
# SET THE COUNTDOWN TIMER
# for simplicity we set it to 3
# We can also take this as input

# Open the camera
def eye_tracking(ret, frame):

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
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    _, threshold = cv2.threshold(gray_roi, 28, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    temp = cv2.addWeighted(roi, 0, black, 100, 0)
    advImg = cv2.add(temp, adv)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cenX = int((x + (x + w)) / 2)
        cenY = int((y + (y + h)) / 2)
        cv2.circle(advImg, (cenX, cenY), 10, (0, 255, 0), -1)

        break

    return  threshold, gray_roi, advImg


cap = cv2.VideoCapture(0)

while True:

    # Read and display each frame
    ret, frame = cap.read()

    # 함수 호출
    threshold, gray_roi, advImg =eye_tracking(ret, frame)

    cv2.imshow("Bin", threshold)
    cv2.imshow("Gray ROI", gray_roi)
    cv2.imshow("Eye tracking", advImg)

    # check for the key pressed
    k = cv2.waitKey(125)

    # set the key for the countdown
    # to begin. Here we set q
    # if key pressed is q
    if k == ord('q'):
        prev = time.time()

        while TIMER > 0:
            ret, frame = cap.read()

            # 함수 호출
            threshold, gray_roi, advImg = eye_tracking(ret, frame)

            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(advImg, str(TIMER), (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
            cv2.imshow("Bin", threshold)
            cv2.imshow("Gray ROI", gray_roi)
            cv2.imshow("Eye tracking", advImg)
            cv2.waitKey(125)

            # current time
            cur = time.time()

            # Update and keep track of Countdown
            # if time elapsed is one second
            # than decrese the counter
            if cur - prev >= 1:
                prev = cur
                TIMER = TIMER - 1

        # else:
        #     ret, frame = cap.read()
        #
        #     # Display the clicked frame for 2
        #     # sec.You can increase time in
        #     # waitKey also
        #     cv2.imshow("Bin", threshold)
        #     cv2.imshow("Gray ROI", gray_roi)
        #     cv2.imshow("Eye tracking", whiteImg)
        #
        #     # time for which image displayed
        #     cv2.waitKey(2000)
        #
        #     # Save the frame
        #     #cv2.imwrite('camera.jpg', img)
        #
        # # HERE we can reset the Countdown timer
        # # if we want more Capture without closing
        # # the camera

    # Press Esc to exit
    elif k == 27:
        break

# close the camera
cap.release()

# close all the opened windows
cv2.destroyAllWindows()