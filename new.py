#importing files
import cv2
import numpy as np
import time
import os
import handmodule as htm
#importing the image folder
folderPath = "header"
mylist = os.listdir(folderPath)
print(mylist)
overlaylist =[]
for impPath in mylist:
    image = cv2.imread(f'{folderPath}/{impPath}')
    overlaylist.append(image)
print(len(overlaylist))
#turnig on camera
header = overlaylist[0]
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
while True:
    success, img = cap.read()
    #flip image
    img = cv2.flip(img,1)

    #import image
    #find landmarkes
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist)!=0:

        print(lmlist)
        # tip of index and middle finger

        x1, y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
    #checking and modifimg fingers




# setting header image
    img[0:158, 0:1280] = header
    cv2.imshow("image",img)
    cv2.waitKey(1)