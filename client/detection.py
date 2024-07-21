from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import pandas as pd
from ultralytics import YOLO
import cvzone
import cv2
import numpy as np 
import time
import requests


class Detection(QThread): 
    def __init__(self, token, location, receiver):
        super(Detection, self).__init__()
        self.token = token
        self.location = location
        self.receiver = receiver
        
    changePixmap = pyqtSignal(QImage)
    
    def run(self):
        self.running = True
        
        model = YOLO('model.pt')
        
        cap = cv2.VideoCapture('final.mp4')
        
        my_file = open("coco1.txt", "r")
        data = my_file.read()
        class_list = data.split("\n") 
        
        count = 0
        starting_time = time.time()
        
        while self.running:
            ret, frame = cap.read()
            
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Skip every 2 frames
            count += 1
            if count % 3 != 0:
                continue
            
            frame = cv2.resize(frame, (1020, 500))
            results = model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")
            
            weeds_detected = False
            
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                if "weeds" in c:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
                    weeds_detected = True
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
            
            # calculating elapsed time
            elapsed_time = starting_time - time.time()
            
            if weeds_detected and elapsed_time <= -10:
                starting_time = time.time()
                self.save_detection(frame)
            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = 3 * 1020
            convertToQtFormat = QImage(rgbImage.data, 1020, 500, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(854, 1480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
                
    def save_detection(self, frame):
        cv2.imwrite("saved_frame/frame.jpg", frame)
        print('Frame Saved')
        self.post_detection()
        
    def post_detection(self):
        try:
            url = 'http://127.0.0.1:8000/api/images/'
            headers = {'Authorization': 'Token ' + self.token}
            files = {'image': open('saved_frame/frame.jpg', 'rb')}
            data = {'user_ID': self.token,'location': self.location, 'alert_receiver': self.receiver}
            response = requests.post(url, files=files, headers=headers, data=data)
            
            if response.ok:
                print('Alert was sent to the server')
                
            else:
                print('Unable to send alert to the server')
                
        except:
            print('Unable to access server')
            
			
             
       
