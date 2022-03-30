import cv2
import os
import cvzone

# Dimensions and variables
width, height = 1280,729
folderPath = "./Presentation"

#Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# Retrieving the list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len) # to sort the images in correct order we use key=len 
# print(pathImages)

imgNumber = 0

# Capturing the frame
while True:
    success, img = cap.read()
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)
    key = cv2.waitKey(1)
    # End the program when we press "q"
    if key == ord("q"):
        break