import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture('../FaceDetection/videos/video1.mp4') # path of the video
pTime = 0

mpDraw = mp.solutions.drawing_utils  # to draw facial points on the face
mpFaceMesh = mp.solutions.face_mesh   # create a facemesh   
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2) # max_num_faces means the number of faces to be detected
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2) # control the thickness of the connection lines and the points we will use ‘drawSpec’.

while True:
    success, img = cap.read()  # read the image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert the img to RGB
    results = faceMesh.process(imgRGB) # pass the RGB img to facemesh
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks: # create a for loop, to draw the detected landmarks on the face
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
        for id,lm in enumerate(faceLms.landmark):
            #print(lm)
            ih, iw, ic = img.shape
            x,y = int(lm.x*iw), int(lm.y*ih)
            print(id,x,y) # will print out the id and coordinates

    cTime = time.time()  
    fps = 1 / (cTime - pTime)  # currenttime-previoustime
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3) # display the framepersecond
    cv2.imshow("Image", img)
    cv2.waitKey(1)


