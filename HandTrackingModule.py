import cv2
import time as t
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1,detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        #print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True ):

        lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo] #handNo 0 will give the first hand
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id,cx,cy]) #the list will have the id and the x,y coordinate of that index
                if draw:
                    cv2.circle(img,(cx, cy), 15, (255, 0, 255), -1)

        return lmList

def main(): #this is the dummy code, copy the main file in each code, and other things will be imported from the header file
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    cap.set(3, 1280)
    cap.set(4, 720)

    detector = handDetector() #already has default parameters

    while True:
        success, img = cap.read()

        img = detector.findHands(img)

        lmList = detector.findPosition(img) #this list will have the coordinates of each point on our hands wil id to it

        if len(lmList) != 0: #coz if no hands are there, there will be no data in list
            print(lmList[4]) #4 is the index of tip of thumb



        cTime = t.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

        cv2.imshow("see", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows




if __name__ == "__main__":
    main()