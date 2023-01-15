import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector as htm
import mediapipe as mp
import HandTrackingModule as htm2
import cvzone
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
ehands = mpHands.Hands()

 

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


def distace(p1, p2):
    d = ((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2)
    d = d**0.5 
    return d

class DragImg():
    def __init__(self, path, posOrigin,):
        self.isTouch=False
        self.posOrigin = posOrigin
        self.path = path
        self.isTouch = False
        #self.arrowback_path = arrowback_path
        self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)

        self.img = cv2.resize(self.img, (0,0),None,0.1,0.1)
        #self.arrowback = cv2.imread(self.arrowback_path,)
        self.firstTouch = 0
        self.size = self.img.shape[:2]

    def update(self, cursor):

        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
            self.firstTouch=1
            self.isTouch = True
        else:
            self.isTouch = False
k=0
i=0
firstTouch =0

# madarchod = cv2.imread(r'/home/ammeh/syntax error/opencv/temp_bg.jpg')
# cv2.imshow('hi', madarchod)
# cv2.waitKey(1000)

og_backgroud = cv2.imread('finalSave.png')



# path = "/home/ammeh/syntax error/trythis"
# myList = os.listdir(path)
# print(myList)
detector = htm(detectionCon=0.8)
scale = 0.24


listImg = DragImg("dart.png",[50,50])
# for x, pathImg in enumerate(myList):
#     imgType = 'png'
#     listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 128, 50]))
pTime = 0

def centerActual(x,y,hdart,wdart):
    xReturn = x-wdart//2
    yReturn = y-hdart//2
    return xReturn,yReturn

def center(x,y,hdart,wdart):  #give origin points and will return the center point
    xThis = x - wdart//2
    yThis = y- hdart//9

    return xThis,yThis

def shrink(inputArrow,inputBg,leavingx,leavingy,scale):
    hArrow,wArrow,_ = inputArrow.shape
    k=0
    scale -= 0.01
    k+=1
        
    # print(k,scale)
    hshow,wshow = int(scale*hArrow), int(scale*wArrow)
    print(hshow,wshow)
    outputArrow = cv2.resize(inputArrow,(hshow,wshow))

    x,y = center(leavingx,leavingy,hArrow,wArrow)
    
    finalxyz = cvzone.overlayPNG(inputBg,outputArrow, (x,y))


    cv2.imshow('hi',finalxyz)
    time.sleep(1)
bhai = cv2.imread(r'finalSave.png')
hBhai,wBhai = bhai.shape[:2]
print(wBhai//2,hBhai//2)

def countScore(xArrow,yArrow,sourceimg):
    dist = distace([xArrow,yArrow],[wBhai//2,hBhai//2])
    range0 = [dist<16,2000]
    range1 = [16<=dist<40,1000]
    range2 = [40<=dist<76,750]
    range3 = [76<=dist<111,500]
    range4 = [111<=dist<148,400]
    range5 = [148<=dist<181,250]
    range6 = [360<=dist<220,100]
    range7 = [dist>220,50]

    rangeList = [range0,range1,range2,range3,range4,range5,range6,range7]

    for i in rangeList:
        if i[0]:
            print(i,dist)
            
            cv2.putText(sourceimg,str(i[1]),(1225-50,385),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            


    





arrowBack = cv2.imread(r"arrowback.png", cv2.IMREAD_UNCHANGED)
oldArrowBackShape = arrowBack.shape

arrowBack = cv2.resize(arrowBack,(0,0), None, 0.24,0.24)
hBackArrow,wBackArrow,_ = arrowBack.shape



#print(bhai)

while True:
    bhai = cv2.imread(r'finalSave.png')
    hBhai,wBhai = bhai.shape[:2]
    success, img = cap.read()

    

    img = cv2.flip(img, 1)
    hands = detector.findHands(img,draw=False, flipType=False)

    # img = detector.findHands(img, draw=True)
    # lmList = detector.findPosition(img, draw = False)

    ##draw hand skeleton
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = ehands.process(imgRGB)
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(bhai, img, handLms, mpHands.HAND_CONNECTIONS)


    try:
        #print(bhai)
        # print(len(listImg))
        if hands:
            lmList = hands[0]['lmList']

            length, _ = detector.findDistance(lmList[8],lmList[4], None)
            if length<45:

                cursor = lmList[8]
                imgObject = listImg
                imgObject.update(cursor)
                firstTouch = imgObject.firstTouch

            pinch = distace(lmList[8],lmList[4])<45

        imgObject=listImg
        h,w = imgObject.size
        ox, oy = imgObject.posOrigin
        if imgObject.isTouch and pinch and firstTouch:
            #print("holding",i)
            final = cvzone.overlayPNG(bhai,arrowBack,[ox,oy])                    
        else:
            final = cvzone.overlayPNG(bhai,imgObject.img, [ox,oy])
        
        #print(firstTouch,i)
        if firstTouch and not pinch and scale>0.02:
            #shrink(arrowBack,final,ox,oy,0.24)
            scale -= 0.01
            k+=1
                
            print(k,scale)
            hshow,wshow = int(scale*oldArrowBackShape[0]), int(scale*oldArrowBackShape[1])
            print(hshow,wshow)
            arrowBack = cv2.resize(arrowBack,(wshow,hshow))

            x,y = center(ox,oy, arrowBack.shape[0],arrowBack.shape[1])

            finalxyz = cvzone.overlayPNG(bhai,arrowBack,(x+41,y+18))
            print(x+41,y+18)
            #finalxyz = cv2.circle(finalxyz,(ox,oy),4,(0,0,0),5)

            cv2.imshow('hi',finalxyz)
            cv2.waitKey(10)

        elif scale<=0.02:
            countScore(x+41,y+18,finalxyz)
            cv2.imshow('hi',finalxyz)
            print(x+41,y+18)
            pass
        else:
            cv2.imshow('hi',final)

            #print("what")
    except:
        ox,oy = 50,50
        x,y = 50,50
        cv2.imshow('hi',final)
        pass

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    #cv2.putText(final, str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
    
    


    #cv2.imshow('hi',final)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    i+=1
    #background = og_backgroud

cap.release()
cv2.destroyAllWindows



