#importing files
import cv2
import numpy as np
import time
import os
import handmodule as htm
#importing the image folder
brushThickness = 12
EraserThikness = 75




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
drawColor = (255,0,255)
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
xp,yp = 0,0
imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    success, img = cap.read()
    #flip image
    img = cv2.flip(img,1)

    #import image
    #find landmarkes
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:



        #print(lmlist)
        # tip of index and middle finger

        x1, y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
    #checking and modifimg fingers
        # check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
    # if selection mode - two fingers up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            print('Selection Mode')
            if y1<125:
                if 250<x1<450:
                    header = overlaylist[2]
                    drawColor =(0,255,0)
                elif 550 < x1 < 750:
                    header = overlaylist[3]
                    drawColor = (255,0, 0)
                elif 880 < x1 < 950:
                    header = overlaylist[1]
                    drawColor = (0, 0, 255)
                elif 1050 < x1 < 1200:
                    header = overlaylist[0] #sa
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            #Drawing Mode - Index finger up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1 ), 15, drawColor,cv2.FILLED)

            print('Drawing Mode')
            if xp==0 and yp==0:
                xp,yp = x1,y1


            if drawColor == (0,0,0):
                cv2.line(img, (xp,yp), (x1,y1),drawColor,EraserThikness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, EraserThikness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img,imgCanvas)







# setting header image
    img[0:125, 0:1280] = header
    cv2.imshow("image",img)
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow('Canvas',imgCanvas)
    cv2.waitKey(1)