'''
import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


def findHands(self, img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if self.results.multi_hand_landmarks:
        for handLms in self.results.multi_hand_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, handLms,
                                           self.mpHands.HAND_CONNECTIONS)

    return img


def findPosition(self, img, handNo=0, draw=True):
    xList = []
    yList = []
    bbox = []
    self.lmList = []
    if self.results.multi_hand_landmarks:
        myHand = self.results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id, lm)
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            xList.append(cx)
            yList.append(cy)
            # print(id, cx, cy)
            self.lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

    xmin, xmax = min(xList), max(xList)
    ymin, ymax = min(yList), max(yList)
    bbox = xmin, ymin, xmax, ymax

    if draw:
        cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                      (0, 255, 0), 2)

    return self.lmList, bbox


def fingersUp(self):
    fingers = []
    # Thumb
    if self.lmList[self.tipIds[0]][1] >self.lmList[self.tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # totalFingers = fingers.count(1)

    return fingers


def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
    x1, y1 = self.lmList[p1][1:]
    x2, y2 = self.lmList[p2][1:]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
        cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

    return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()'''

#Importing openCV, mediapipe and time libraries
import cv2
import mediapipe as mp
import time


#Creating a Class/prototype
class handDetector():

    #Constructor, with some default values
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon=trackCon

        #Assigning the hand detector as well as hand landmarks(points) detector funtions to variables of the class
        self.mpHands= mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    #function to detect hands and place/draw landmarks on them
    def findHands(self, img, draw=True):
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results =  self.hands.process(img1)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    #Function to find coordinates of all the landmarks of a particular hand(default= hand number 0). Returns a list of all of them.
    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):

                #To draw those handlandmarks on the video frames
                #The coordinates recieved in lm are actually relative, i.e, 0-1. So, we need to convert them as per the size of original image.

                #Getting height, width and the number of channels of the original images using the .shape function
                height, width, channels = img.shape

                #Converting the relative coordinates(x,y) from lms to original coordinates(cx,cy)
                cx,cy = int(lm.x*width), int(lm.y*height)

                #print(id, cx, cy)
                self.lmList.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 10, (255,255,0), cv2.FILLED)

        return self.lmList

    def fingersUp(self): #checks whether the finger are up or not
        fingers=[]
        tipIDs=[4,8,12,16,20] #Finger tip IDs

        #thumb
        if self.lmList[tipIDs[0]][1]< self.lmList[tipIDs[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for id in range(1,5):
            if self.lmList[tipIDs[id]][2]> self.lmList[tipIDs[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
        #it returns a list (0 if it's up and 1 if it's not).

#Note: To change the color of Landmark joining lines
#Use this below mentioned instead of line number 31
#self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, self.mpDraw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),self.mpDraw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4))

#Implementation/Check
def main():
    pTime = 0
    cTime = 0
    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        #FRAME RATE
        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0),3)

        cv2.imshow("Hello", img)
        #TO TERMINATE THE PROGRAM, PRESS Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
              break

if __name__=="__main__":
    main()