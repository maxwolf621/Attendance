import datetime
import time
import cv2 
import argparse
import numpy as np
import imutils
import requests,re
import sqlite3
from DBinsert import dbinsert


def islate():
    '''
        To check the time for attendance of employee
        if the employee is late or not...
    '''
    now = datetime.datetime.now()
    today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if(now >= today8am):
        return 'yes'
    else:
        return 'no'

def face_sets():
    ID = 0  #initilize ID
    name = "" #initilize Name
    emp_id = ['5150', '5157', '3157', '6157', '4'] #employee's ID  
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognise via LBPHF method
    recognizer.read('trained.yml')  #to load the training data 
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    
     # if false_counter >= 10 then the system would take a shot
     # to mark the person who has been taked as 'Suspicious Person'
    false_counter = 0

    #Motion detection
    ap = argparse.ArgumentParser()
    ap.add_argument("-area", type=int, default=200000) 
    ret = vars(ap.parse_args())
    
    vs = cv2.VideoCapture(0)
    vs.set(3, 640)  #set Width
    vs.set(4, 480)  #set Height
    minW = 0.2*vs.get(3)  #set minWidth
    minH = 0.2*vs.get(4)  #set minHeight
    print("Camera is Staring")
    firstFrame = None
    print("Start")
    
    while(1):
        retval,img =vs.read()
        if img is None : #check the camera 
            print("HARDWARE alert!! check your camera")
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray sacle
        grey = cv2.GaussianBlur(gray, (21, 21), 0)   #blur
        
        if firstFrame is None: # initialize
            firstFrame = gray
            continue
        # Comparing with current image and referrence image
        frameDelta = cv2.absdiff(firstFrame, grey)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        faces = faceCascade.detectMultiScale(  
            gray,  
            scaleFactor = 1.2,  
            minNeighbors = 5,  
            minSize = (int(minW), int(minH)),  
            )

        for obj_contour in cnts:
            if cv2.contourArea(obj_contour) < ret["area"]: 
                continue
            else:
                for(x,y,w,h) in faces:
                    '''
                        To recognize employee 
                        if not employee it would take a picture \
                             and store in the directory
                    '''
                    ID, confidence = recognizer.predict(gray[y:y+h,x:x+w]) 
                    distance = round(100 - confidence)
                    if (distance > 50):
                        '''
                            record the time and name of employee \
                                 and update the data base
                        '''
                        print('access')
                        ID = emp_id[ID]              
                        empid= ID
                        try:
                            on_date= f'{time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday}'
                            on_time= f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
                        except UnboundLocalError as e :
                            print(e.args)
                        is_late=islate()
                        a = dbinsert(on_time,on_date,is_late,empid,"site.db")
                        a.insert()
                        #requests.post(url='http://127.0.0.1:5001/attendance', json=to_api)
                        false_counter = 0
                    else:
                        '''
                            take a shot for the Suspicious person
                        '''
                        ID = 'unknown'
                        print('access denied')
                        false_counter +=1
                        if false_counter ==10:
                            cv2.imwrite("unknown/" + f'{time.localtime().tm_hour}:{time.localtime().tm_min}' + ".jpg" , img)
                            false_counter = 0
                    cv2.rectangle(img, (x,y), (x+w,y+h), (170,255,200), 10)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img,str(ID),(x+5,y-5), font, 1, (255, 255, 255), 2)
                    cv2.putText(img, str(distance), (x+5,y+h-5), font, 1, (255,255,0), 1)

            # for motion detection 
            (a, b, c, d) = cv2.boundingRect(obj_contour)
            cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0), 2)

            # display the image
            cv2.imshow('motion_detector',img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    vs.release()
    cv2.destroyAllWindows()
                

if __name__ =='__main__' :
    face_sets()
