# encoding:utf-8
import requests
import base64
client_id = 'jO83mibjqItqUZfijp6MnpYF'
client_secret = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
response = requests.get(host)
if response:
    t = response.json()
    access_token = t['access_token']

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/multi_object_detect"
# 二进制方式打开图片文件
f = open('C:/Users/Brandon/Pictures/课表.png', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())