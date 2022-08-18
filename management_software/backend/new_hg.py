
import time
import cv2
print(cv2.__version__)
import numpy as np
import pickle
import mediapipe as mp
 
class mpHands:

    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
                                        self.detectionCon, self.trackCon)
    def Marks(self,frame):
        myHands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands
def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    palmSize=((handData[0][0]-handData[9][0])**2+(handData[0][1]-handData[9][1])**2)**(1./2.)
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            distMatrix[row][column]=(((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.))/palmSize
    return distMatrix
 
def findError(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    print(error)
    return error
def findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol):
    errorArray=[]
    for i in range(0,len(gestNames),1):
        error=findError(knownGestures[i],unknownGesture,keyPoints)
        errorArray.append(error)
    errorMin=errorArray[0]
    minIndex=0
    for i in range(0,len(errorArray),1):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture='Unknown'
    return gesture
 
 
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(1)
time.sleep(5)
keyPoints=[0,4,5,9,13,17,8,12,16,20]
 
train=int(input('Enter 1 to Train, Enter 0 to Recognize '))
if train==1:
    trainCnt=0
    knownGestures=[]
    numGest=int(input('How Many Gestures Do You Want? '))
    gestNames=[]
    for i in range(0,numGest,1):
        prompt='Name of Gesture #'+str(i+1)+' '
        name=input(prompt)
        gestNames.append(name)
    print(gestNames)
    trainName=input('Filename for training data? (Press Enter for Default) ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
if train==0:
    trainName=input('What Training Data Do You Want to Use? (Press Enter for Default) ')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
    with open(trainName,'rb') as f:
        gestNames=pickle.load(f)
        knownGestures=pickle.load(f)
 
tol=10
 
while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    handData=findHands.Marks(frame)
    if train==1:
        if handData!=[]:
            print('Please Show Gesture ',gestNames[trainCnt],': Press t when Ready')
            if cv2.waitKey(1) & 0xff==ord('t'):
                knownGesture=findDistances(handData[0])
                knownGestures.append(knownGesture)
                trainCnt=trainCnt+1
                if trainCnt==numGest:
                    train=0
                    with open(trainName,'wb') as f:
                        pickle.dump(gestNames,f)
                        pickle.dump(knownGestures,f)
    if train == 0:
        if handData!=[]:
            unknownGesture=findDistances(handData[0])
            myGesture=findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol)
            #error=findError(knownGesture,unknownGesture,keyPoints)
            cv2.putText(frame,myGesture,(100,175),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
            myGesture=myGesture+'\r'
            return myGesture
            
    for hand in handData:
        for ind in keyPoints:
            cv2.circle(frame,hand[ind],25,(255,0,255),3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()