from sre_constants import SUCCESS
import mediapipe as mp
import cv2 as cv2
import time

capture = cv2.VideoCapture(0)  # 0 is given for webcam

mpHands = mp.solutions.hands # to detect the hands
hands = mpHands.Hands() # the number of hands to detect is set to 2, minimum detection confidence is 0.5 and the minimum tracking confidence is 0.5
mpDraw = mp.solutions.drawing_utils # to draw the key points.

pTime = 0
cTime = 0

while True:
    success, img = capture.read()  # read the image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert the image to RGB
    results = hands.process(imgRGB) # detect hands in the frame
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for hndLandmarks in results.multi_hand_landmarks:
            for id, lndmark in enumerate(hndLandmarks.landmark):
                print(id,lndmark)

                # height, width, centre positions
                h, w, c = img.shape
                # cx, cy are the positions
                cx, cy = int(lndmark.x * w), int(lndmark.y * h)
                print(id, cx, cy)

                if id == 4:   #( 4 is the tip of a thumb)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    # highlight the dots in the keypoints using cv2.circle

            mpDraw.draw_landmarks(img, hndLandmarks, mpHands.HAND_CONNECTIONS)
                    # connect the key points using mpDraw.draw_landmarks

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
