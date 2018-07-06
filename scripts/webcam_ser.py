#!/usr/bin/env python3
import numpy as np
from flask import Flask
import time
from flask import render_template
from flask import request
import base64
from PIL import Image
from io import StringIO, BytesIO
import robo_talker
import sys
sys.path[3], sys.path[9] = sys.path[9], sys.path[3]
import cv2
from sensor_msgs.msg import Image
import datetime

sys.path.append('./DB_Helper')
from DB_Helper.DB_Helper import *
db_conn = get_db_conn()

def extract_face_features(gray_face, wd=96, ht=96):
    gray_face = cv2.resize(gray_face, (wd, ht))
    gray_face = cv2.equalizeHist(gray_face)
    gray_face = cv2.GaussianBlur(gray_face, ksize=(3, 3),
                                    sigmaX=0, sigmaY=0)

    gray_face = np.array(gray_face, dtype=np.float64)
    gray_face_vector = gray_face.reshape(wd * ht, order='C')
    return gray_face_vector

app = Flask(__name__)

@app.route('/')
def webcam():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    print('getting data from web.')
    if request.method == 'POST':
        image_b64 = request.form['img']
        robo_talker.talker(image_b64)
        imgdata = base64.b64decode(image_b64)
        with open('img/org_img.jpg', 'wb') as f:
            f.write(imgdata)
        # imgdata = cv2.imread('img/org_img.jpg')

        # imgdata = cv2.cvtColor(imgdata, cv2.COLOR_BGR2GRAY) 
        # face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
        # faces = face_cascade.detectMultiScale(
        #                                     imgdata,
        #                                     scaleFactor=1.15,
        #                                     minNeighbors=5,
        #                                     minSize=(5, 5)  # ,
        #                                             # flags=cv2.CV_HAAR_SCALE_IMAGE
        #                                                 )
        # for i, (x, y, w, h) in enumerate(faces):
        #     cv2.rectangle(imgdata, (x, y), (x + w, y + w), (255, 0, 0), 2)
        #     gray_face = imgdata[y:y+h, x:x+w]
        #     gray_face_vector = extract_face_features(gray_face)
        #     gray_face = gray_face_vector.reshape((96, 96))
        #     cv2.imwrite('./gray_face.jpg', gray_face)
			
        global db_conn
        time.sleep(5)
        if robo_talker.MSG != None:
            result = robo_talker.MSG
            robo_talker.MSG = None 

            #DB_Handler
            sql = "select * from Cars where licence = %s"
            car = None
            with db_conn.cursor() as cursor:
                cursor.execute(sql, (result))
                car = cursor.fetchone()
                db_conn.commit()
            print(car)
            if (car == None):
                cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(cur_time)
                sql = "insert into Cars (licence, time) values(%s, %s);"
                with db_conn.cursor() as cursor:
                    cursor.execute(sql, (result, cur_time))
                    db_conn.commit()
                return "Welcome~ " + result + "\nEnter at " + cur_time
            else:
                park_time = datetime.datetime.strptime(car['time'],'%Y-%m-%d %H:%M:%S')
                cur_time = datetime.datetime.now()
                sql = "delete from Cars where licence = %s"
                with db_conn.cursor() as cursor:
                    cursor.execute(sql, (result))
                    db_conn.commit()
                return result + " has parked for " + str(round((cur_time-park_time).seconds/60, 2)) + " minutes"
        else:
            return "Can't recognize"
        #with open('pic.jpg', 'wb') as f:
        #    f.write(imgdata)
    #return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, ssl_context='adhoc')
