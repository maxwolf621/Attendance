

#將圖像轉成matrix
import numpy as np
#圖像轉換用
from PIL import Image


#例如利用os.chdir(路徑)來轉換任何你要讀取的檔案
import os
import cv2

#存放臉部資料庫的路徑
Sample_path = 'EmployeeSampleData/'

#訓練演算法
recognizer = cv2.face.LBPHFaceRecognizer_create() 

#辨識演算法
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

def get_SamplesandIDLables(path):
    
    '''將你輸入的pathu以及path底下的每個檔案路徑做結合'''
    '''例如你的path是/home/pi/Downloads/PJ/EmployeeSampleData'''
    '''底下有xxx_1,jpg,xxx2.jpg.....'''
    '''則經過os.path.join(path,f)變成/home/pi/Downloads/PJ/EmployeeSampleData/xxx_1,'''
    '''此方法叫做list Comprehension'''
    imagePaths = [
    os.path.join(path,sub) for sub in os.listdir(path)
    ]
    
#     print(imagePaths)
    
    #存放每張matrix化的人臉sample
    face_list =[]
    #幫人臉Sample做Label來做分類
    ids   =[]

    for imagePath in imagePaths:

        #將face samples色彩單一化
        PIL_img = Image.open(imagePath).convert('L')
        #samples每個pixel以array顯示（也就是matrix）
        img_numpy = np.array(PIL_img,'uint8')
        
        #辨識人臉資料庫內的人臉
        faces = detector.detectMultiScale(img_numpy)

        #取檔名的編號
        #例如你的人臉資料庫的檔案名為 face_1_4則以利用以下的function會回傳4則 id = int(4)
        id = int(os.path.split(imagePath)[-1].split("_")[1])
#         print(os.path.split(imagePath)[-1].split("_")[1])
        
        #開始辨識每張人臉samples並存入faces,ids的list內
        for (x,y,w,h) in faces:
            face_list.append(img_numpy[y:y+h,x:x+w]) 
            #將你命名好的人臉samples放入ids list內
            ids.append(id)
    return face_list,ids

#訓練
face_list,ids = get_SamplesandIDLables(Sample_path)
recognizer.train(face_list, np.array(ids))

#指定學習完後產生的yml檔案路徑
#yml為學習後的檔案給cv2.face.LBPHFaceRecognizer_create().read(trained.yml)用
recognizer.write('trained.yml')

#顯示以訓練幾個人臉
print(f'{len(np.unique(ids))} faces trained')


