# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 22:09:29 2018

@author: Sanket
"""


import cv2
import numpy as np
import os
import mysql.connector
from datetime import date

# Open database connection
db = mysql.connector.connect(
                     host = "localhost",
                     user ="root",
                     password="",
                     database="college" )

course_id = 0
semester = 0

# prepare a cursor object using cursor() method
cursor = db.cursor()

# to get the details of course_id and semester
cursor.execute("SELECT course_id , semester FROM selection_of_course where id = 1")
data = cursor.fetchone();
course_id = data[0]
semester = data[1]



# to fetch the details of students
cursor.execute("SELECT * FROM student_details WHERE SEMESTER = %s", (semester,))

student_id=[]
student_name=[]


data = cursor.fetchall()
sum = 0
for row in data:
    student_id.append(row[0])
    student_name.append(row[1])

print(student_id)
print(student_name)


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

def collect_dataset():
    images = []
    labels = []
    labels_dic = {}
    
    people = [person for person in os.listdir("people/")]
    
    for i , person in enumerate(people):
        labels_dic[i] = person
        for image in os.listdir("people/"+person):
            images.append(cv2.imread("people"+"/"+person + "/"+image,0))
            labels.append(i)
            
    return (images , np.array(labels),labels_dic)       


images , labels , labels_dic = collect_dataset()




rec_lbph = cv2.face.createLBPHFaceRecognizer()
rec_lbph.train(images , labels)

print("Done")

cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("xml/haarcascade_frontalface_default.xml")



while True:
     ret, frame = cap.read()
     index=-1   
     if ret: 
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_coord = detector.detectMultiScale(frame_gray,1.3,5)
            #print(len(face_coord))
            
           # print(face_coord)
            
            if len(face_coord):
                faces = cut_faces(frame, face_coord)
                faces = normalize_intensity(faces)
                faces = resize(faces)
                #print(len(face_coord))   
                
                for i , face in enumerate(faces):
                    collector = cv2.face.MinDistancePredictCollector()
                    rec_lbph.predict(face,collector)
                 
                    conf = collector.getDist()
                    pred = collector.getLabel()   
                    print("conf=", conf,"pred=",pred)
                    threshold = 115
                    if conf < threshold:
                        std_id =int(labels_dic[pred])
                        if std_id in student_id:
                            index = student_id.index(std_id)
                            print(index)
                            name=student_name.__getitem__(index)
                           # print(name)
                        else:
                            name = 'unknown'
                            
                        if len(face_coord) == 1 :#input attendance if and only iff the face value is 1
                                print('Here')
                                save = (str(date.today()),std_id,course_id)
                                try:#in order to avoid multiple entries error
                                    cursor.execute("INSERT INTO attendance_tracker VALUES  (%s, %s, %s)",save)
                                    
                                    db.commit()
                                except:
                                    print('Attendance is already marked')
                                for(x , y, w, h) in face_coord:
                                    cv2.rectangle(frame , (x,y) , (x+w , y+h),
                                                  (150 , 150 , 0) ,5
                                                  )
                                    cv2.putText(frame, name,        
                                                (x+10, y-10),
                           
                                    cv2.FONT_HERSHEY_PLAIN, 1.5 ,(66,53,243),2, cv2.LINE_AA
                    
                                    )
                                
                        else:
                            cv2.putText(frame, "One Face Only!",        
                                                (100,100),
                           
                            cv2.FONT_HERSHEY_PLAIN, 1.5 ,(66,53,243),2, cv2.LINE_AA
                                    
                            )
                            
                       
                    else:
                        print("No face data")
                        
                
                  
                    
            cv2.imshow("Face Recognition System",frame)

     if  cv2.waitKey(40) & 0xff == 27:
            break;

cursor.close()            
db.close()

cap.release()
cv2.destroyAllWindows()            
        
                        
                    