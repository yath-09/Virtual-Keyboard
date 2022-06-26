'''Using cvzone version 1.5.3 and Mediapipe Version  0.8.9.1
   HandTrackingModule is used to track hand and find positions of index tips
   Algo used- Matching the button position and index finger tip position to check keyboard position
   Clicking using indexfinger and thumb tip joining which is measured by distance between them
   Pynput used for typing in other tabs such as google,notepad'''

''' importing required modules'''
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector    #https://google.github.io/mediapipe/solutions/hands
from time import sleep
from pynput.keyboard import Controller # For Keyboard linking with other tabs

cap= cv2.VideoCapture(0)
cap.set(3, 1490)

detector = HandDetector(detectionCon=0.8) # improving the quality of detection
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Bk"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "Et"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Cp"],
        [' ']]

keys1 = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "Bk"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "Et"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Cp"],
        [' ']]


finalText = ""
finaltext1=""  # used here for backspace
keyboard = Controller()
def drawAll(img, buttonList): # for drawing the keys of keyboard
    for button in buttonList:
        x, y = button.pos   # extracting position of buttons
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []

#displaying  keyboard on screen
for i in range(len(keys)):     # loop in loop for generating keyboard
    for j, key in enumerate(keys[i]):   # enumerate index value and value
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
caps= 0
#main
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img) # https://www.youtube.com/watch?v=3xfOa4yeOb0
    img = drawAll(img, buttonList)

    if hands:
        lmList = hands[0]['lmList'] # list of landmarks of first hand 0 for 1st hand
        #lmList1 = hands[1]['lmList']  # list of landmarks of first hand 1 for 2nd hand
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 8, y - 8), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, ( 0, 0, 255), 4)

                l, _, img = detector.findDistance(lmList[8], lmList[4], img)
                #l1, _, img = detector.findDistance(lmList[8], lmList[4], img)

                ## when clicked
                # first backspace condition then keyboard one
                if l < 17 and button.text == 'Bk':
                    keyboard.press("\b") # the keyword for backspace
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)
                    len1 = len(finalText)
                    i=0
                    finaltext1 = ''
                    while len1>1 : # removing last letter of string
                        finaltext1 +=finalText[i]
                        i +=1
                        len1 -=1
                    finalText = finaltext1
                    sleep(0.28)
                elif l< 17 and button.text == 'Cp':
                    buttonList = []
                    if caps==0:
                        caps=1
                        for i in range(len(keys1)):  # loop in loop for generating keyboard
                            for j, key in enumerate(keys1[i]):  # enumerate index value and value
                                buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
                        img = drawAll(img, buttonList)
                    elif caps==1:
                        caps=0
                        for i in range(len(keys)):  # loop in loop for generating keyboard
                            for j, key in enumerate(keys[i]):  # enumerate index value and value
                                buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
                        img = drawAll(img, buttonList)
                    sleep(0.28)

                elif l < 17 and button.text == 'Et':
                    keyboard.press("\n")  # the keyword for enter
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)
                    finalText = ''

                elif l < 17: # as distance becomes less that intention to click and choose
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)

                    finalText += button.text
                    sleep(0.28)

    cv2.rectangle(img, (50, 567), (1200, 660), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 640), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
