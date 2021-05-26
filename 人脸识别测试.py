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

# 注册人脸
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
# params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"group_id\":\"group_repeat\",\"user_id\":\"user1\",\"user_info\":\"abc\",\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"}"
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())

# 搜索人脸
