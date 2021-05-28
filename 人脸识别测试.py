import base64
import cv2
import numpy
import requests
from aip import AipFace

APP_ID = '24250074'
API_KEY = 'jO83mibjqItqUZfijp6MnpYF'
SECRET_KEY = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'
client = AipFace(APP_ID,API_KEY,SECRET_KEY)

def getToken():
    client_id = 'jO83mibjqItqUZfijp6MnpYF'
    client_secret = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        t = response.json()
        access_token = t['access_token']
    return access_token

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    rval,det = cap.read()
    det2 = numpy.rot90(det)
    cv2.imwrite('SearchPic.jpg',det2)
    f = open('SearchPic.jpg',"rb")
    pic = base64.b64encode(f.read())
    image = str(pic, 'utf-8')
    image_type = "BASE64"
    group_id_list = "group1"
    response = client.search(image,image_type,group_id_list)
    if response:
        print(response["result"]["user_list"][0]["group_id"])  # 用户组名称
        print(response["result"]["user_list"][0]["user_id"])  # 用户ID
        print(response["result"]["user_list"][0]["score"])  # 相似度
