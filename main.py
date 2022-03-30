import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Dimensions and variables
width, height = 1280,720
folderPath = "./Presentation"

#Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# Retrieving the list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len) # to sort the images in correct order we use key=len 
# print(pathImages)

# Slide Variables
imgNumber = 0
hs, ws = int(120*1),int(213*1)
gestureThreshold = 350
buttonPressed = False
buttonCounter = 0
buttonDelay = 10
annotations = [[]]
annotationNumber = -1
annotationStart = False

# Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

# Capturing the frame
while True:
    success, img = cap.read()
    # Flipping the image in horizontal for slide navigation convenience
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Implement hand detection in Image
    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold), (width,gestureThreshold),(0,255,0),10)

    # Slide navigate
    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand["center"]
        # print(fingers)
        lmList = hand["lmList"]

        # Constrain pointer values for drawing
        xVal = int(np.interp(lmList[0][0],[width//2,width], [0,width]))
        yVal = int(np.interp(lmList[0][1],[250,height-150],[0,height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold: #if hand is at the height of the face
            # annotationStart = False
            # Gesture-1 - Left
            if fingers == [1,0,0,0,0]:
                # print("Left")
                annotationStart = False
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    buttonPressed = True
            # Gesture-2 - Right
            if fingers == [0,0,0,0,1]:
                # print("Right")
                annotationStart = False
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    buttonPressed = True
        # Gesture-3 - Show Pointer
        if fingers == [0,1,1,0,0]:
            # print("Pointer")
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            annotationStart = False
        # Gesture-4 - Draw Pointer
        if fingers == [0,1,0,0,0]:
            # print("Draw")
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False
        # Gesture-5 - Eraser
        if fingers == [0,1,1,1,0]:
            # print("Erase")
            if annotations:
                if annotationNumber >= -1:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True
    else:
        annotationStart = False

    # Button pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # Draw all annotations
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!= 0:
                cv2.line(imgCurrent,annotations[i][j-1], annotations[i][j], (0,0,200),12)

    # Adding Webcam Image on the slides
    imgSmall = cv2.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    # putting the image on the top right corner of the slides
    imgCurrent[0:hs, w-ws:w] = imgSmall


    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)
    key = cv2.waitKey(1)
    # End the program when we press "q"
    if key == ord("q"):
        break