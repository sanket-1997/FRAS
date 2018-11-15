#face recognition system

"@Developer Sanket Kumar Srivastava"



import numpy as np
import cv2
import os
from matplotlib import pyplot as plt


def resize(images , size = (50,50)):
    images_norm = []
    for image in images:
        image_norm = cv2.resize(image,size,interpolation=cv2.INTER_AREA)
        images_norm.append(image_norm)
        
    return images_norm    

def cut_faces(image, face_coord):
    faces = []
     
    for(x , y , w , h) in face_coord:
            w_r = int(0.2*w/2)
            faces.append(image[y:y+h,x+w_r:x+w-w_r])
            
    
    return faces        




def normalize_intensity(images):
    images_norm=[]
    for image in images:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image))
    
    return images_norm    





folder = "people/" + input('Roll No: ').lower()#input name
cv2.namedWindow("Face Recognition System",cv2.WINDOW_AUTOSIZE)
cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("xml/haarcascade_frontalface_default.xml")
if not os.path.exists(folder):
    os.makedirs(folder)  
    counter =0 
    timer = 0
    while counter<20:
        #to capture the video
        print(counter)    
        #detector of the features 
        # capture frame-by-frame
        ret, frame = cap.read()    
        if ret: # check ! (some webcam's need a "warmup")
        # our operation on frame come here
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_coord = detector.detectMultiScale(frame_gray,1.3,5)
            #print(face_coord)
            
            if len(face_coord) and timer%100==50:
                faces = cut_faces(frame , face_coord)
                faces = normalize_intensity(faces)
                faces = resize(faces)
                cv2.imwrite(folder+'/'+str(counter) + '.jpg',faces[0])
    
                counter+=1
            for(x , y, w, h) in face_coord:
                cv2.rectangle(frame , (x,y) , (x+w , y+h),
                              (150 , 150 , 0) ,8
                              )
            cv2.imshow('frame',frame)
            cv2.waitKey(50)
            timer+=25
else:
    print("This roll no. already exist")                



cap.release()
cv2.destroyAllWindows()
# When everything is done release the capture
