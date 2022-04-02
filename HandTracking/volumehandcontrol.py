import cv2
import time
import numpy as np
from sympy import N
import volumehndtracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(0)   #Checks for camera
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)

#To access speaker through the library pycaw 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()   #If camera works capture an image
    img = detector.findHands(img)   
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
       # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]     #thumb
        x2, y2 = lmList[8][1], lmList[8][2]      #index finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        #creating circle at the tips of thumb and index finger
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  #image #fingers #radius #rgb
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)       #create a line b/w tips of index finger and thumb
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)                     #distance b/w tips using hypotenuse
        print(length)
        # Hand range 50 - 300
        # Volume Range -65 - 0
        # from numpy we find our length,by converting hand range in terms of volume range 
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length<=50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # creating a volume bar       
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # for the percentage
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xff==ord(' '): #By using spacebar delay will stop
        break
        
cap.release()     #stop cam       
cv2.destroyAllWindows() #close window