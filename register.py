from aip import AipFace
import base64

""" 你的 APPID AK SK """
from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '24250074'
API_KEY = 'jO83mibjqItqUZfijp6MnpYF'
SECRET_KEY = 'xNFDBFafiFuRXPMAObwMv1rOcq38Yh8s'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


f = open('test.jpg', 'rb')
pic = base64.b64encode(f.read())
image = str(pic, 'utf-8')

imageType = "BASE64"

groupId = "group1"

userId = "user1"

""" 如果有可选参数 """
options = {}
options["user_info"] = "123"
options["quality_control"] = "NORMAL"
options["liveness_control"] = "LOW"
options["action_type"] = "REPLACE"

""" 带参数调用人脸注册 """
result = client.addUser(image, imageType, groupId, userId, options)
print(result)
