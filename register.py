# encoding:utf-8
import requests
import base64
from aip import AipFace
import cv2
import json
client_id = 'jO83mibjqItqUZfijp6MnpYF'
client_secret = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'
APP_ID='24250074'
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
response = requests.get(host)
if response:
    t = response.json()
    access_token = t['access_token']

client = AipFace(APP_ID, client_id, client_secret)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
image = base64.b64encode(frame).decode()
face_add = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token='+access_token
headers = {
    'Content-Type': 'application/json'
}
data = {
    'image': image,
    'image_type': 'BASE64',
    'group_id': 'archive',
    'user_id': 'zhang',
}
res = requests.post(url=face_add, headers=headers, data=data)
res = json.loads(res.text)
print(res)
