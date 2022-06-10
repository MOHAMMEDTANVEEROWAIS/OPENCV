import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui

def AiVirtualMouseProject():
        ###############
        wCam, hCam = 640, 480
        frameR = 100 #Frane Reduction
        smoothening = 7
        ###############

        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture(1)
        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()
        # print(wScr, hScr)



        while True:
            # 1.Find the Hand Landmarks
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, )
            # print(lmList)

            # 2.Get the tip of the Index and Middle Fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                x4, y4 = lmList[4][1:]
                # x5, y5 = lmList[4][1:]
                # print(x1,y1,x2,y2)

                # 3. Check which finger are up
                fingers = detector.fingersUp()
                # print(fingers)
                cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 3)

                # 4. Only Index finger : Moving Mode
                if fingers[1] == 1 and fingers[2] == 0:
                    # 5.Convert coordinates
                    # cv2.rectangle(img, (frameR, frameR), (wCam-frameR), (hCam-frameR), (255,0,255), 3)
                    x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

                    # 6.Smoothen Values
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    # 7.Move Mouse
                    autopy.mouse.move(wScr-clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                # 8.Both Index and Middle Fingers are up : Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1:

                    # 9.Find distance between fingers
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    print(length)

                    # 10.Click Mouse if distance is Short
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        # autopy.mouse.click(button: Button=RIGHT, delay: float=None)
                        # autopy.mouse.click(button: Button=None, delay: float=None)
                        autopy.mouse.click()
                        # pyautogui.click(button='right')

                # F.Both Index and Middle Fingers are up : Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1:

                    # 9.Find distance between fingers
                    length, img, lineInfo = detector.findDistance(4, 8, img)
                    print(length)

                    # 10.Click Mouse if distance is Short
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 255), cv2.FILLED)
                        # autopy.mouse.click(button: Button=RIGHT, delay: float=None)
                        # autopy.mouse.click()
                        pyautogui.click(button='right')




                # 11.Frame Rate
                cTime = time.time()
                fps = (cTime - pTime)
                pTime = cTime
                # fps = "FRAMES PER SECOND"
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # 12.Display



                cv2.imshow("AIVirtualMouseProject", img)
                cv2.waitKey(1)







