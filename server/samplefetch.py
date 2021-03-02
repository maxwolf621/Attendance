import cv2
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# Counts of (face)samples
count = 0
cam = cv2.VideoCapture(0) 
cam.set(3, 640)
cam.set(4, 480)
#Enter employee's ID
face_id = input("enter employee id:")
print("Look at Camera")

while True:
    ret, img = cam.read()  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #灰階取樣
    
    #using haarcascade_frontalface_default.xml to detect a human face
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x,y,w,h) in faces:
        
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) 
        
        count += 1
        print(count) 
        #End the program when 100 fotos have been taken
        if count == 100:
            print("fetch ends")
        else:
            print("next one")
        
        cv2.imshow("Face Sample Fetch", img)
  
        #(gray[y:y+h,x:x+w]) only store the picture with "face"
        cv2.imwrite("EmployeeSampleData/face_" + str(face_id) + '_' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        
    
    if cv2.waitKey(100) & 0xff == ord("q"): 
        print("Exit")
        break
    elif count >= 100 : 
        break
cam.release()
cv2.destroyAllWindows()
