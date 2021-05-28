# encoding:utf-8
import RPi.GPIO as GPIO
import time
import cv2
from aip import AipFace
import numpy
import base64
import requests
import json
from jsonpath import jsonpath

SCK=[7,37,16,40]
DT=[11,35,18,38]
APP_ID = '24250074'
API_KEY = 'jO83mibjqItqUZfijp6MnpYF'
SECRET_KEY = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
token = ''

def getToken():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
    response = requests.get(host)
    if response:
        t = response.json()
        access_token = t['access_token']
    return access_token

def calweight(idx):
    value = 0
    initWeight = 0
    nowWeight = 0
    flag = 1
    time.sleep(0.09)
    for i in range(24):
        GPIO.output(SCK[idx],1)
        if(0==GPIO.input(SCK[idx])):
            time.sleep(0.09)
        value = value<<1
        GPIO.output(SCK[idx],0)
        if GPIO.input(DT[idx])==1:
            value = value+1
    GPIO.output(SCK[idx],1)
    GPIO.output(SCK[idx],0)
    time.sleep(0.09)
    if flag == 1:
        flag = 0
        initWeight = value
    else:
        nowWeight = abs(value-initWeight)
    return nowWeight

def camerapos(idx):#摄像头定位餐品
    res=[]
    cap = cv2.VideoCapture(idx)
    rval,frame = cap.read()
    img = frame
    sp = img.shape
    x1 = int(sp[0]*0.28)
    x2 = int(sp[0]*1.00)
    y1 = int(sp[1]*0.10)
    y2 = int(sp[1]*0.55)
    dst = img[y1:y2,x1:x2]
    grey = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    dilation = cv2.dilate(grey,element1)
    erosion = cv2.erode(dilation,element1)
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
    dilation = cv2.dilate(erosion,element2)
    cv2.imwrite("pospic.jpg",dilation)
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/multi_object_detect"
    # 二进制方式打开图片文件
    f = open('pospic.jpg', 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        raw = response.text
        print(raw)
        json_data = json.loads(raw)
        result = (json_data.get('result'))
        top = jsonpath(json_data, "$..top")
        height = jsonpath(json_data, "$..height")
        width = jsonpath(json_data, "$..width")
        left = jsonpath(json_data, "$..left")
        for i in range(len(top)):
            res.append([top[i],height[i],width[i],left[i]])
        return res

def faceSearch(idx):#人脸识别
    cap = cv2.VideoCapture(idx)
    rval, det = cap.read()
    det2 = numpy.rot90(det)
    cv2.imwrite('SearchPic.jpg', det2)
    f = open('SearchPic.jpg', "rb")
    pic = base64.b64encode(f.read())
    image = str(pic)
    image_type = "BASE64"
    group_id_list = "group1"
    response = client.search(image, image_type, group_id_list)
    if response:
        if response["result"]["user_list"][0]["score"]>60:
            return (response["result"]["user_list"][0]["user_id"],response["result"]["user_list"][0]["user_info"])

if __name__=='__main__':
    token = getToken()
    try:
        idnum,username = faceSearch(0)
        if idnum<-1:
            print("该用户未注册")
        else:
            print(username)
    except:
        print("no user")
    print(camerapos(1))
