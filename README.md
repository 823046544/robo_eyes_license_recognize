
# Robo_Eyes_license_recognize System

一个基于ROS平台的车库管理系统

项目实现基于flask轻量级Python的Web框架，利用OpenCV进行摄像头图片截取以及保存。

通过HyperLPR实现车牌识别、数字文字分割以及识别

##功能实现

* 1 flask轻量级框架+OpenCV实现屏幕录制截图（像素存在一点小问题~）

![这里写图片描述](https://img-blog.csdn.net/20180706125128555?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x6aDgyMzA0NjU0NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

* 2 HyperLPR 通过训练好的级联分类器进行车牌是识别以及数字识别

```Python

import HyperLPR_.HyperLPRLite as pr
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

```

![这里写图片描述](https://img-blog.csdn.net/20180706125653861?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x6aDgyMzA0NjU0NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

* 3 利用 pymql 连接数据库

```python
def get_db_conn():
    global g_db_connection
    if g_db_connection is None or not checkConn(g_db_connection):
        g_db_connection = pymysql.connect(host=config.DATABASE['host'], port=config.DATABASE['port'], user=config.DATABASE['user'], password=config.DATABASE['password'], db=config.DATABASE['db'], cursorclass=pymysql.cursors.DictCursor, charset='utf8')
    return g_db_connection

get_db_conn()
```
其中config.py为数据库信息，下载后可以根据本地mysql进行修改
```
DATABASE = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'db': '',
}

```

###模拟进入

![这里写图片描述](https://img-blog.csdn.net/20180706130451403?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x6aDgyMzA0NjU0NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

###模拟离开

![这里写图片描述](https://img-blog.csdn.net/20180706130539491?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2x6aDgyMzA0NjU0NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
