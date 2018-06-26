import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time

def SpeedTest(image_path):
    grr = cv2.imread(image_path)
    model = pr.LPR("HyperLPR/model/cascade.xml", "HyperLPR/model/model12.h5", "HyperLPR/model/ocr_plate_all_gru.h5")
    model.SimpleRecognizePlateByE2E(grr)
    t0 = time.time()
    for x in range(20):
        model.SimpleRecognizePlateByE2E(grr)
    t = (time.time() - t0)/20.0
    print "Image size :" + str(grr.shape[1])+"x"+str(grr.shape[0]) +  " need " + str(round(t*1000,2))+"ms"

    

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
fontC = ImageFont.truetype("HyperLPR/Font/platech.ttf", 14, 0)

def drawRectBox(image,rect,addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0,0, 255), 2,cv2.LINE_AA)
    cv2.rectangle(image, (int(rect[0]-1), int(rect[1])-16), (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
                  cv2.LINE_AA)
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((int(rect[0]+1), int(rect[1]-16)), addText.decode("utf-8"), (255, 255, 255), font=fontC)
    imagex = np.array(img)
    return imagex


import HyperLPR.HyperLPRLite as pr
import cv2
import numpy as np
import csv
print ('read')
grr = cv2.imread("img/org_img.jpg")
print ('succeed read')
model = pr.LPR("HyperLPR/model/cascade.xml","HyperLPR/model/model12.h5","HyperLPR/model/ocr_plate_all_gru.h5")
for pstr,confidence,rect in model.SimpleRecognizePlateByE2E(grr):
    print confidence
    if confidence>0.5:
        image = drawRectBox(grr, rect, pstr+" "+str(round(confidence,3)))
        cv2.imwrite("./img/upload_org_img.jpg", image)
        print "plate_str:"
        print pstr
        print "plate_confidence"
        print confidence
        outfile = "./data.csv"
        out = open(outfile, 'w')
        out.write(pstr)
            
# cv2.imshow("image",image)
# cv2.waitKey(0)



# SpeedTest("images_rec/2_.jpg")
